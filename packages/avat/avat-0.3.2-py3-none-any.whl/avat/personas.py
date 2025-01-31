import requests
import json
from icecream import ic
ic.configureOutput(prefix=' \n ', includeContext=False)
from .api_request import ApiRequest
from .utils import get_av_headers, get_eval_data, get_persona_data, get_chat_headers, get_base_url, get_eval_headers
import concurrent.futures
import time

def parse_agent_reply(agent_response):
    # Parse the agent reply from the REST API response
    if "agent_reply" in agent_response.json():
        return agent_response.json()["agent_reply"]
    else:
        raise Exception("No agent_reply in response")
    
def get_tot_eval_scores(tot_eval_scores, n_runs, verbose=True):

        accuracy_scores = {}
        aggregate_score = 0

        if verbose: print("\nEval Results for " + str(n_runs) + " chats:")
        for ev,score in tot_eval_scores.items():
            acc = round(score / n_runs, 3)
            s_acc = str(acc)
            accuracy_scores[ev] = s_acc
            if verbose: print(ev + ": " + s_acc)
            aggregate_score += acc

        aggregate_score = str(round(aggregate_score / len(tot_eval_scores), 3))

        return accuracy_scores, aggregate_score

def compute_score(evals_response, verbose=False):

        if type(evals_response) == dict:
            evals_response = evals_response["evals"]
        else:
            evals_response = evals_response.json()["evals"]

        accuracy_count = 0
        tot_count = 0

        if len(evals_response) == 0:
            return ""
        
        log = "########################### \nMessage to evaluate: \n"
        log += evals_response[0]["msg_to_eval"] + "\n"
        log += "########################### \nEvaluation: \n"

        eval_scores = {}

        for eval in evals_response:

            tot_count += 1
            result = eval["eval_result"]

            score = 0
            if "pass" in result.lower():
                score = 1
                
            accuracy_count += score

            if "eval_question" in eval:
                log += result + ": " + str(eval["eval_question"]) + "\n"
                eval_scores[eval["eval_question"]] = score

            elif "eval_tag" in eval:
                log += result + ": " + str(eval["eval_tag"]) + "\n"
                eval_scores[eval["eval_tag"]] = score

        log += "########################## \nAccuracy: \n"
        log += str(accuracy_count) + "/" + str(tot_count) + "\n"

        if verbose:
            print(log)
        return accuracy_count, tot_count, eval_scores
    
class Simulator():

    def __init__(self, auth_token, env="cloud"):
        self.auth_token = auth_token
        self.env = env


        self.base_url = get_base_url(env)
        self.evals_url = self.base_url + 'run_msg_eval/'
        self.evals_run_update_url = self.base_url + 'update_eval_run/'
        self.persona_url = self.base_url + 'chat/'
        self.create_evals_run_url = self.base_url + 'create_eval_run/'

        self.evals_headers = get_eval_headers(auth_token)
        self.persona_headers = get_av_headers(auth_token)
        self.chat_headers =  get_chat_headers(auth_token)

    
    def evaluate(self, chat_session_id):

        # Get whole chat
        chat_url = self.base_url + 'get_chat/' + "?chat_session_id=" + chat_session_id
        chat_response = ApiRequest(chat_url, self.chat_headers).get()
        #ic(chat_response.json())
        whole_chat = str(chat_response.json()['previous_conversation'])
        

        # Eval whole chat
        evals_response = ApiRequest(self.evals_url, self.evals_headers, get_eval_data(whole_chat, chat_session_id, self.custom_eval_questions, self.standard_eval_tags)).post()
        evals_run_response = ApiRequest(self.evals_run_update_url, self.evals_headers, {"run_id": self.run_id, "eval_chat_ids": [chat_session_id,]}).post()

        accuracy_count, tot_count, eval_scores = compute_score(evals_response, verbose=False)

        return accuracy_count, tot_count, eval_scores
        

    def chat_with_my_agent(self,  
                    n_max_turns_per_chat=1, 
                    n_chats_per_persona=1,  # chats per persona
                    personaSet_id="671e876cb93db3a0c724b1d5", 
                    run_eval = True,
                    to_eval={}, 
                    agent_endpoints = ("", "", ""), 
                    agent_persona_mes_key = "persona_msg", 
                    json_flag=True,
                    eval_every_message=False,
                    agent_response_parser=parse_agent_reply, 
                    start_chat_endpoints=None,
                    start_chat_fields_to_msg=[]
                    ):
        

        self.personaSet_id = str(personaSet_id)
        self.personaSet = get_personaSet(self.personaSet_id, self.auth_token, env=self.env)
        n_personas = int(self.personaSet.json()["n_personas"])
        n_tot_chats = n_chats_per_persona * n_personas

        self.agent_url, self.agent_headers, self.agent_data = agent_endpoints
        ev_run_data = {"n_runs":str(n_tot_chats), "tot_eval_scores": {}, "aggregate_score": "0", "n_personas":str(n_personas)}
        evals_run = ApiRequest(self.create_evals_run_url, self.evals_headers, ev_run_data).post().json()

        run_id = evals_run["eval_run_id"]        
        tot_eval_scores = {}    

        self.run_eval = run_eval
        self.agent_persona_mes_key = agent_persona_mes_key
        self.n_max_turns_per_chat = n_max_turns_per_chat
        self.eval_every_message = eval_every_message
        self.run_id = run_id
        self.custom_eval_questions = to_eval["custom_eval_questions"]
        self.standard_eval_tags = to_eval["standard_eval_tags"]
        self.json_flag = json_flag
        self.agent_response_parser = agent_response_parser
        self.start_chat_endpoints = start_chat_endpoints
        self.start_chat_fields_to_msg = start_chat_fields_to_msg
        
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
            persona_run = [executor.submit(self._chat_with_my_agent, 
                                        ) for run_n in range(0, n_chats_per_persona)]
            
            for future in concurrent.futures.as_completed(persona_run):
                correct_count, tot, eval_scores = future.result()
                
                for ev,score in eval_scores.items():
                    if ev in tot_eval_scores:
                        tot_eval_scores[ev] += score
                    else:
                        tot_eval_scores[ev] = score
        
        

        accuracy_scores, aggregate_score = get_tot_eval_scores(tot_eval_scores, n_tot_chats)
        evals_run_response = ApiRequest(self.evals_run_update_url, self.evals_headers, {"run_id": run_id, "tot_eval_scores": accuracy_scores, "aggregate_score": aggregate_score}).post()

    def _chat_with_my_agent(self):

        correct_count = 0
        tot = 0        
        combined_eval_scores = {}

        # If the agent need to start the chat with an API call, do it here.
        if self.start_chat_endpoints:
            start_chat_url, start_chat_headers, start_chat_data = self.start_chat_endpoints
            new_chat_session = ApiRequest(start_chat_url, start_chat_headers, start_chat_data).post()
            for api_field in self.start_chat_fields_to_msg:
                self.agent_data[api_field[1]] = new_chat_session.json()[api_field[0]]


        ### Simulate 
        self.persona_ids = self.personaSet.json()["persona_ids"]

        with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
            sim_and_ev = [executor.submit(self._sim_and_eval, 
                                           persona_id 
                                        ) for persona_id in self.persona_ids]
            
            for future in concurrent.futures.as_completed(sim_and_ev):
                accuracy_count, tot_count, eval_scores = future.result()
                       
                correct_count += accuracy_count
                tot += tot_count
                combined_eval_scores = {x: combined_eval_scores.get(x, 0) + eval_scores.get(x, 0) for x in set(combined_eval_scores).union(eval_scores)}

        return correct_count, tot, combined_eval_scores
    

    def _sim_and_eval(self, persona_id):

        ic("Start Simulation")
        av = get_persona(persona_id, self.auth_token, env=self.env)
        persona_first_message = av.json()["first_message"]
        self.agent_data[self.agent_persona_mes_key] = persona_first_message

        self.agent_data["is_new_chat"] = True
        #ic(self.agent_data)
        agent_response = ApiRequest(self.agent_url, self.agent_headers, self.agent_data, json_flag=self.json_flag).post()
        agent_response = self.agent_response_parser(agent_response)
        ic(agent_response)
        
        persona_data = get_persona_data(new_chat=True,agent_msg=agent_response, persona_id=persona_id)
        persona_response = ApiRequest(self.persona_url, self.persona_headers, persona_data).post()
        persona_reply = persona_response.json()["persona_reply"]
        ic(persona_reply)

        chat_session_id = persona_response.json()["chat_session_id"]
        self.agent_data["chat_session_id"] = chat_session_id # to support the dummy agent
        self.agent_data[self.agent_persona_mes_key] = persona_reply
        

        for i in range(0, self.n_max_turns_per_chat):
            
            self.agent_data["is_new_chat"] = False
            self.agent_data["chat_session_id"] = chat_session_id
            agent_response = ApiRequest(self.agent_url, self.agent_headers, self.agent_data, json_flag=self.json_flag).post()
            agent_response = self.agent_response_parser(agent_response)
            ic(agent_response)

            persona_data = get_persona_data(new_chat=False, chat_session_id=chat_session_id,agent_msg=agent_response, persona_id =persona_id)
            persona_response = ApiRequest(self.persona_url, self.persona_headers, persona_data).post()
            persona_reply = persona_response.json()["persona_reply"]
            ic(persona_reply)
            is_last_persona_message = persona_response.json()["is_last_message"]

            self.agent_data[self.agent_persona_mes_key] = persona_reply 

            if is_last_persona_message:
                break
        
        ### Eval 
        
        if self.run_eval:
            accuracy_count, tot_count, eval_scores = self.evaluate(chat_session_id)
        else:
            accuracy_count, tot_count, eval_scores = 0, 0, {}

        return accuracy_count, tot_count, eval_scores




def get_persona(persona_id, auth_token, env="cloud"):

    base_url = get_base_url(env)
    persona_url = base_url + 'personas/' + persona_id
    persona_headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + auth_token,
    }
    persona = ApiRequest(persona_url, persona_headers).get()
    return persona

def create_persona(auth_token, persona_profile, env="cloud"):

    base_url = get_base_url(env)
    persona_url = base_url + '/personas'
    persona_headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + auth_token,
    }

    persona_info = ApiRequest(persona_url, persona_headers, persona_profile).post()
    return persona_info.json()

def get_personaSet(personaSet_id, auth_token, env="cloud"):

    base_url = get_base_url(env)
    personaSet_url = base_url + 'personasets/' + personaSet_id
    personaSet_headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + auth_token,
    }
    personaSet = ApiRequest(personaSet_url, personaSet_headers).get()
    return personaSet

def create_personaSet(auth_token, personaSet_profile, env="cloud"):

    base_url = get_base_url(env)
    personaSet_url = base_url + '/personasets'
    personaSet_headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + auth_token,
    }

    personaSet_info = ApiRequest(personaSet_url, personaSet_headers, personaSet_profile).post()
    return personaSet_info.json()