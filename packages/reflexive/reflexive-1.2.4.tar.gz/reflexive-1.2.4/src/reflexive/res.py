import json
from pandas import DataFrame
from spacy import displacy
from time import sleep
from reflexive import Config
from reflexive import AWS
from reflexive import S3
from reflexive import Comprehend
from reflexive import Nlp
from reflexive import Display
from reflexive import RES_graph

class Res_analyse:
    
    config:Config
    aws:AWS
    s3:S3
    comprehend:Comprehend
    nlp:Nlp
    
    def __init__(self,aws_profile="default") -> None:
        return self._setup(aws_profile)
    
    def _setup(self,aws_profile) -> None:
        self.config = Config(aws_profile)
        self.config.set_parameters(name_prefix="RES")
        self.aws = AWS(self.config)
        return None
    
    def set_parameters(self,
                       s3_access_point:str,
                       s3_bucket_name:str,
                       comprehend_service_role_name:str,
                       reflexive_entity_name:str,
                       reflexive_entity_version:str) -> str:
        self.config.set_s3_parameters(s3_access_point,s3_bucket_name)
        self.config.set_comprehend_parameters(comprehend_service_role_name)
        self.config.set_comprehend_custom_entity_parameters(reflexive_entity_name,reflexive_entity_version)
        params = self.config.get_parameters()
        return json.dumps(params, indent=2)
    
    def setup_aws(self) -> None:
        # Create a new S3 client
        self.s3 = S3(self.aws)
        # Create a new Comprehend client
        self.comprehend = Comprehend(self.aws)
        # Create an Nlp object to perform analysis on the text
        self.nlp = Nlp(self.aws)
        return None
    
    def get_basic_analytics(self,df:DataFrame) -> DataFrame:
        
        # Text length - this is needed for comprehend analytics
        df = self.nlp.text_length(df)
        #df = nlp.remove_IQR_outliers(df)
        # Comprehend analysis
        results = self.nlp.comprehend_analysis(self.comprehend,df)
        #print(results)
        errors = self.nlp.check_results(results)
        #print(errors)
        if errors=={}:
            print("No errors, so adding results to dataframe")
            df = self.nlp.add_results_to_df(results,df)
            df = self.nlp.comprehend_analytics(df)
        return df
    
    def get_reflexive_analytics(self,df:DataFrame) -> DataFrame:
        # Reflexive expression analysis
        response = self.nlp.analyse_reflexive_expressions(df,self.s3,self.comprehend)
        #print(response)
        job_id = self.comprehend.get_current_job_id()
        print("Job ID:",job_id)
        status = self.comprehend.check_job_status()
        print("Status:",status)

        # Get the details of the job
        # details = comp.get_job_details()
        # print("Job details:",details)

        inc = 0
        while status=="SUBMITTED" or status=="IN_PROGRESS":
            print("Waiting 10 seconds...")
            sleep(10)
            status = self.comprehend.check_job_status()
            print(f"Job status {inc}:",status)
            inc += 1
            
        # Download from S3 and extract results 
        print("Downloading and extracting results...")
        results = self.comprehend.download_and_extract(self.s3)
        print("RESULTS:")
        print(results)
        
        # Extract output of analysis and add to df
        return self.nlp.add_to_dataframe(df,results)

class Res_display:
    
    res_analyse:Res_analyse
    vis:Display
    
    def __init__(self,res:Res_analyse) -> None:
        return self._setup(res)
    
    def _setup(self,res:Res_analyse) -> None:
        self.res_analyse = res
        self.vis = Display(res.aws)
        return None  
    
    def show_text(self,df:DataFrame,inline=True) -> str:
        df = self.vis.add_offsets(df)
        disp_data = self.vis.create_displacy(df)
        if inline:
            displacy.render(disp_data,manual=True,style="ent", options=self.res_analyse.config.display_options)
            html_out = "Set inline to false to produce HTML"
        else:
            html_out = displacy.render(disp_data,manual=True,style="ent", options=self.res_analyse.config.display_options,page=True,jupyter=False)
        return html_out
    
    def get_interactions(self,df:DataFrame) -> DataFrame:
        #Get RE sequence
        df = self._add_res_sequence(df)
        df = self._add_res_interactions(df)
        df = self._add_res_adj_matrix(df)
        return df
    
    def show_graph(self,df:DataFrame,inline=True) -> str:
        for am in df.res_adj_matrix:
            g = RES_graph(am)
            g.show()
        return("nothing yet")
    
    def _add_res_sequence(self,df):
        temp_df = df.copy()
        temp_df['res_sequence'] = temp_df.reflexive_expressions.apply(self._get_res_sequence)
        return temp_df
    
    def _add_res_interactions(self,df):
        temp_df = df.copy()
        temp_df['res_interactions'] = temp_df.res_sequence.apply(self._count_res_interactions)
        return temp_df
    
    def _add_res_adj_matrix(self,df):
        temp_df = df.copy()
        temp_df['res_adj_matrix'] = temp_df.res_interactions.apply(self._create_adj_matrix)
        return temp_df
    
    def _get_res_sequence(self,reflexive_expressions):
        re_seq = [label for re,label in reflexive_expressions]
        res_seq = []
        # Need to substitute new RES labels for old RE labels
        for re in re_seq:
            if re=='ER' or re=='VR':
                res_seq.append('NR')
            elif re=='EV':
                res_seq.append('EP')
            elif re=='CN':
                res_seq.append('AF')
            else:
                res_seq.append(re)
        return res_seq
    
    def _empty_res_interactions(self) -> dict[tuple,int]:
        RE_types = ['RR','NR','AR','AF','EP']
        RE_interactions:dict[tuple,int] = dict()
        for t1 in RE_types:
            for t2 in RE_types:
                entry = tuple(sorted((t1,t2)))
                if entry not in RE_interactions.keys():
                    RE_interactions[entry] = 0
        return RE_interactions
    
    def _count_res_interactions(self,re_sequence:list[str]) -> dict[tuple,int]:
        re_ints = self._empty_res_interactions()
        limit = len(re_sequence)-1
        for i,s in enumerate(re_sequence):
            if i < limit:
                rei = tuple(sorted((s,re_sequence[i+1])))
                #print(i,rei)
                re_ints[rei] += 1 
        return re_ints
    
    def _create_adj_matrix(self,interactions:dict[tuple,int])->list[list[int]]:
        re_types = ["RR","NR","AR","AF","EP"]
        matrix = []
        for r in re_types:
            row = []
            for c in re_types:
                key = tuple(sorted((r,c)))
                #print(key)
                weight = interactions.get(key,0)
                row.append(weight)
            matrix.append(row)
        return matrix
        
        
        
        