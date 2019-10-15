

import math

from heart_test.anser_anls.base_anls import BaseAnls
from django.forms.models import model_to_dict


class Scl_90():

    def __init__(self,answer = None):
        
        #BaseAnls.__init__(self,answer)
        #super(BaseAnls).__init__(self,answer)
        self.answer = answer
        self.point = {
            "躯体化" : {
                "db_name" : "body",
                "project" : [1,4,12,27,40,42,48,49,52,53,56,58],
                "score" : 1.45 + 0.49
            },
            "强迫" : {
                "db_name" : "qiangpo",
                "project" : [3,9,10,28,38,45,46,51,55,65],
                "score" : 1.99 + 0.64
            },
            "人际敏感" : {
                "db_name" : "renji",
                "project" : [6,21,34,36,37,41,61,69,73],
                "score" : 1.98 + 0.74
            },
            "抑郁" : {
                "db_name" : "yiyu",
                "project" : [5,14,15,20,22,26,29,30,31,32,54,71,79],
                "score" : 1.83 + 0.65
            },
            "焦虑" : {
                "db_name" : "jiaolv",
                "project" : [2,17,23,33,39,57,72,78,80,86],
                "score" : 1.64 + 0.59
            },
            "敌对" : {
                "db_name" : "didui",
                "project" : [11,24,63,67,74,81],
                "score" : 1.77 + 0.68
            },
            "恐怖" : {
                "db_name" : "kongbu",
                "project" : [13,25,47,50,70,75,82],
                "score" : 1.46 + 0.53
            },
            "偏执" : {
                "db_name" : "pianzhi",
                "project" : [8,18,43,68,76,83],
                "score" : 1.85 + 0.69
            },
            "精神病" : {
                "db_name" : "jingshenbing",
                "project" : [7,16,35,62,77,84,85,87,88,90],
                "score" : 1.63 + 0.54
            },
        }

    def anls(self):
        anwser_result = []
        for i in self.point:
            result = {}
            current_point_anwser = []
            for idx in self.point[i]['project']:
                current_point_anwser.append(self.answer[idx - 1])
            pinjun = self.get_pinjun(current_point_anwser)
            result['point']  = i
            result['pinjun'] = round(pinjun,4)
            result['answer'] = current_point_anwser
            result['project'] = self.point[i]['project']
            result['biaozhun'] = self.point[i]['score']
            if result['pinjun'] >= self.point[i]['score']:
                result['is_health'] = False
            else:
                result['is_health'] = True
            anwser_result.append(result)
        return anwser_result
            
    def get_pinjun(self,current_point_anwser):
        current_point_score = sum(current_point_anwser)
        pinjunfen = current_point_score / len(current_point_anwser)
        return pinjunfen

    def get_health(self,input_list):
        result = {}
        for li in input_list:
            for i in self.point:
                if i not in result:
                    result[i] = {
                        "health" : 0,
                        "ill" : 0
                    }
                current_point_answer = []
                for idx in self.point[i]['project']:
                    current_point_answer.append(li[idx - 1])
                pinjun = self.get_pinjun(current_point_answer)
                if pinjun >= self.point[i]['score']:
                    result[i]["ill"] += 1
                else:
                    result[i]['health'] += 1
        return result

    def parse_item_data(self,input_list):
        #model_dic = model_to_dict(query_set)
        result = {}
        for i in self.point:
            current_point_answer = []
            for idx in self.point[i]['project']:
                current_point_answer.append(input_list[idx - 1])
            if self.get_pinjun(current_point_answer) >= self.point[i]['score']:
                result[self.point[i]['db_name']] = 1
            else:
                result[self.point[i]['db_name']] = 0
        return result

    # def get_pinjun_biaozhuncha(self,current_point_anwser):
    #     pinjunshu = self.get_pinjun(current_point_anwser)
    #     pinjun_sum = 0
    #     for i in current_point_anwser:
    #         pinjun_sum += (i - pinjunshu) ** 2 
    #     return math.sqrt(pinjun_sum) , pinjunshu
        
