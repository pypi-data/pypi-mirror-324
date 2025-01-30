from graph_tool.all import (
    Graph,
    graph_draw,
    ungroup_vector_property,
    group_vector_property
)
import cairo

from spacy import displacy

from reflexive import session
from reflexive import cfg

class Display:
    aws:session.AWS = None
    config:cfg.Config = None
    
    defaults = {
        "priority_tags": [
            "NR",
            "AR",
            "RR",
            "EP",
            "AF",
            "TE",
        ],
        "colours": {
            "NR": "#ED1B23",
            "AR": "#00A64F",
            "RR": "#00AEEF",
            "EP": "#FFF200",
            "AF": "#EC008C",
            "TE":"#f7f7d4",
        }
    }
    
    #FFF200 yellow
    #EC008C magenta
    #00AEEF cyan
    #00A64F green
    #ED1B23 red
    
    # "VR_ER": "#ff6644", #Orange
	# 	"AR": "#00cc00", #Green
	# 	"RR": "#6699ff", #Blue
	# 	"EP_EV": "#aacc33", #Lime
	# 	"AF_CN": "#dd44cc", #magenta
	# 	"EO":"#f7f7d4", #light yellow 
	# 	"EA":"#d9f2f2" #light Cyan
    # {
    #     "priority_tags": ["VR_ER","AR","RR","EP_EV","AF_CN","KP"],
    #     "colours": {"VR_EV_CN": "#ff6644","ER_AF": "#dd44cc","AR": "#00cc00","EP": "#aacc33","RR": "#00aaff","KP":"#aaaacc"}}
    
    def __init__(self,aws):
        self.aws = aws
        self.aws = aws
        self.config = self.aws.config
        self.set_default_parameters()
    
    def set_default_parameters(self):
        priority_tags = self.defaults['priority_tags']
        colours = self.defaults['colours']
        options = {"ents": list(colours.keys()), "colors": colours}
        self.config.set_display_parameters(priority_tags,colours,options)
       
     
    def add_reflexive_offsets(self,df):
        temp_df = df.copy()
        temp_df['reflexive_offsets'] = temp_df.ReflexiveResults.apply(self.collect_reflexive_offsets)
        return temp_df
        
    def add_keyphrase_offsets(self,df):
        temp_df = df.copy()
        temp_df['keyphrase_offsets'] = temp_df.KeyPhraseResults.apply(self.collect_keyphrase_offsets)
        return temp_df
    
    def add_syntax_offsets(self,df):
        temp_df = df.copy()
        temp_df['syntax_offsets'] = temp_df.SyntaxResults.apply(self.collect_syntax_offsets)
        return temp_df
    
    def add_offsets(self,df):
        df = self.add_reflexive_offsets(df)
        df = self.add_keyphrase_offsets(df)
        return self.add_syntax_offsets(df)
    
    def create_displacy(self,df):
        all_ents = list(df.apply(self.render_record,axis=1))
        #html_out = displacy.render(all_ents,manual=True,style="ent", options=options,page=True,jupyter=False)
        # with open(f"{path}{prefix}annotated_reflections{postfix}.html","w") as fp:
        #     fp.write(html_out)
        #displacy.render(all_ents,manual=True,style="ent", options=options)
        return all_ents
            
    def render_record(self,record,title="----"):
        #timestamp = record['timestamp'].split('T')[0]
        #pseudonym = record['pseudonym']
        #point_round = record['point_round']
        #title = f"{pseudonym} ({point_round}) - {timestamp}"
        title = f"Idx_{record.name}"
        tags = self.config.display_priority_tags
        text = record['text']
        reflexive_offsets = record['reflexive_offsets']
        keyphrase_offsets = record['keyphrase_offsets']
        syntax_offsets = record['syntax_offsets']
        ents = []
        taken = []
        offsets = []
        for tag in tags:
            if tag in reflexive_offsets:
                offsets = reflexive_offsets[tag]
            elif tag in syntax_offsets:
                offsets = syntax_offsets[tag]
            elif tag in keyphrase_offsets:
                offsets = keyphrase_offsets[tag]
            
            for off in offsets:
                new_ent = {}
                if off[0] in taken:
                    # the start offset is taken
                    x = None
                elif off[1] in taken:
                    # the end offset is taken
                    x = None
                else:
                    # both start and end is available
                    for t in range(off[0],(off[1]+1)):
                        taken.append(t)
                    #print(taken)
                    new_ent["start"] = off[0]
                    new_ent["end"] = off[1]
                    new_ent["label"] = tag
                    ents.append(new_ent)

        text_ents = {
            "text": text, #.replace('\r\n','\n'),
            "ents": ents,
            "title": title
        }

        return text_ents
    
    def collect_keyphrase_offsets(self,krs):
        new_krs = {}
        for kr in krs:
            if kr['Score']>0.98:
                new_krs.setdefault("KP",[]).append((kr['BeginOffset'],kr['EndOffset']))
        return new_krs

    def collect_reflexive_offsets(self,rrs):
        new_rrs = {}
        for rr in rrs:
            if rr['Score']>0.5:
                ent_type = rr['Type']
                if ent_type in ['VR','ER']:
                    label = "NR"
                elif ent_type in ['EP','EV']:
                    label = "EP"
                elif ent_type in ['CN','AF']:
                    label = "AF"
                else:
                    label = ent_type
                new_rrs.setdefault(label,[]).append((rr['BeginOffset'],rr['EndOffset']))
        return new_rrs
    
    def collect_syntax_offsets(self,syntax_results):
        offsets = {}
        for sr in syntax_results:
            pos = sr['PartOfSpeech']
            if pos['Score']>0.99:
                if pos['Tag'] in ['NOUN','ADJ']: # TE - Topic Entity
                    offsets.setdefault("TE",[]).append((sr['BeginOffset'],sr['EndOffset']))
                # if pos['Tag'] in ['ADV','VERB']:
                #     offsets.setdefault("EA",[]).append((sr['BeginOffset'],sr['EndOffset']))
        return self.concatenate_offsets(offsets)
    
    def concatenate_offsets(self,offsets:dict):
        new_offsets = {}
        for k in offsets.keys():
            #print("TAG:",k)
            #print("Offsets:",len(offsets[k]))
            b,e = offsets[k][0] # set to first tag
            for v in offsets[k]:
                #print("b,e",b,e)
                #print("offset:",v)
                if v[0] <= (e+1): # this tag extends a previous tag
                    e = v[1]
                    #print("extending")
                    #print("new_offset:",(b,e))
                else:   # this tag starts a new tag
                    #print("new tag")
                    new_offsets.setdefault(k,[]).append((b,e))
                    b = v[0]
                    e = v[1]
            #print("New offsets:",len(new_offsets[k]))
        return new_offsets
    
class RES_text:
    
    def __init__(self):
        self._setup()
        
    def _setup(self):
        return None
    
    def show(self):
        #displacy.render(disp_data,manual=True,style="ent", options=cfg.display_options)
        return None
     
class RES_graph:
    
    #
    gt_props = {0:{ "lbl":"RR",
                    "pos":(0.2,6.5),
                    "clr":"#00AEEF"},
                1:{ "lbl":"NR",
                    "pos":(5,10),
                    "clr":"#ED1B23"},
                2:{ "lbl":"AR",
                    "pos":(9.8,6.5),
                    "clr":"#00A64F"},
                3:{ "lbl":"AF",
                    "pos":(7.9,1),
                    "clr":"#EC008C"},
                4:{ "lbl":"EP",
                    "pos":(2.1,1),
                    "clr":"#FFF200"}}
                
    
    # re_props = {"RR":{
    #                 "idx": 0,
    #                 "pos":(0.2,6.5),
    #                 "clr":"#00AEEF"},
    #             "NR":{
    #                 "idx": 1,
    #                 "pos":(5,10),
    #                 "clr":"#ED1B23"},
    #             "AR":{
    #                 "idx": 2,
    #                 "pos":(9.8,6.5),
    #                 "clr":"#00A64F"},
    #             "AF":{
    #                 "idx": 3,
    #                 "pos":(7.9,1),
    #                 "clr":"#EC008C"},
    #             "EP":{
    #                 "idx": 4,
    #                 "pos":(2.1,1),
    #                 "clr":"#FFF200"}}
    
    #
    edges = dict()
    #
    iso_vertices = set()
    #
    v_label = None
    #
    v_color = None
    #
    v_pos = None

    #
    def __init__(self,matrix=None):
        self._setup(matrix)
    
    #    
    def _setup(self,matrix):
        if matrix:
            # Edges from matrix
            self.edges = self._matrix_to_dict(matrix)
            self.graph = Graph(g=self.edges.keys(),directed=False)
            self.e_weight = self.graph.new_ep("double",vals=self.edges.values())
            # Handle colour of isolated vertices
            default_clrs = self._get_prop_values('clr')
            actual_clrs = []
            for i in range(5):
                if i in self.iso_vertices:
                    clr = "#cccccc"
                else:
                    clr = default_clrs[i]
                actual_clrs.append(clr)
            self.v_color = self.graph.new_vp("string",vals=actual_clrs)
        else:
            # No edges
            self.graph = Graph(g=self._empty_edge_dict(),directed=False)
            self.e_weight = self.graph.new_ep("double")
            self.v_color = self.graph.new_vp("string",val="#cccccc")
        # Vertex properties common to all graphs    
        self.v_label = self.graph.new_vp("string",vals=self._get_prop_values('lbl'))
        self.v_pos = self.graph.new_vp("vector<double>",vals=self._get_prop_values('pos'))
        
        

    #
    def _matrix_to_dict(self,matrix):
        edges = {}
        for r,row in enumerate(matrix):
            # if empty row, add to iso_vertices
            if sum(row) == 0:
                self.iso_vertices.add(r)
            else:
                for c,weight in enumerate(row):
                    if weight > 0:
                        edge = tuple(sorted((r,c)))
                        #print("r,c:",edge," - ",weight)
                        edges[edge] = weight
        return edges
    
    #
    def _empty_edge_dict(self):
        empty_edges = {}
        for idx in self.gt_props.keys():
            empty_edges[idx] = []
        return empty_edges
    
    #
    def _get_prop_values(self,key):
        values_list =  self.gt_props.values()
        return [p[key] for p in values_list]
    
    # flip coordinates for graph-tool
    def _flipY(self,vpositions):
        x, y = ungroup_vector_property(vpositions, [0, 1])
        y.fa *= -1
        y.fa -= y.fa.min()
        return group_vector_property([x, y])
    
    #
    def show(self,inline=True):
        graph = self.graph
        positions = self._flipY(self.v_pos)
        labels = self.v_label
        colors = self.v_color
        weights = self.e_weight
        graph_draw(graph, inline=inline,output_size=(300,300),fit_view=0.7,
                        pos=positions, 
                        vertex_text=labels,
                        vertex_font_family="sans serif",
                        vertex_font_size=18,
                        vertex_font_weight=cairo.FONT_WEIGHT_BOLD,
                        vertex_fill_color=colors,
                        vertex_size = 50,
                        vertex_halo=False,
                        vertex_pen_width=1.2,
                        vertex_color="#999999",
                        edge_pen_width=weights)
        
    def get_vertex_labels(self):
        return self._get_prop_values('lbl')
    
    def get_vertex_colours(self):
        return self._get_prop_values('clr')
    
    def get_vertex_positions(self):
        return self._get_prop_values('pos')