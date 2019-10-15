
class BaseAnls:
    def __init__(self,anser):
        self.anser = anser

    def get_symptom_num(self):
        positive_num = 0
        all_positive_score = 0
        negative_num = 0
        all_negative_score = 0
        all_score = 0
        for i in self.anser:
            if self.anser[i] >= 2:
                positive_num += 1
                all_positive_score += self.anser[i]
            else:
                negative_num += 1
                all_negative_score += self.anser[i]
            all_score += self.anser[i]
        return round(all_score/len(self.anser),2),positive_num,negative_num,round(all_positive_score/positive_num,2),round(all_negative_score/negative_num,2)

    