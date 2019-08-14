#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@Author:liuyang
"""
class SegmenterEvaluation():

    def __init__(self, id2label_dict):
        self.id2label_dict = id2label_dict

    def evaluate(self, original_labels, predict_labels,segment_ids):
        right, predict,original_labels,predict_labels  = self.get_order(original_labels, predict_labels,segment_ids)
        right_count = self.rightCount(right, predict)
        if right_count == 0:
            recall = 0
            precision = 0
            f1 = 0
            error = 1
        else:
            recall = right_count / len(right)
            precision = right_count / len(predict)
            f1 = (2 * recall * precision) / (precision + recall)
            error = (len(predict) - right_count) / len(right)
        return precision, recall, f1, error, right, predict,original_labels,predict_labels

    def rightCount(self, rightList, predictList):
        count = set(rightList) & set(predictList)
        return len(count)

    def get_order(self, original_labels, predict_labels,segment_ids):

        #orginal_len = 0
        #for i in segment_ids:
        #    if i == 0:
        #        orginal_len=orginal_len+1
            
        #original_labels=original_labels[0:orginal_len]
        #predict_labels=predict_labels[0:orginal_len]
        
        
        original_labels = [self.id2label_dict[id] for id in original_labels if id!=0]
        predict_labels = [self.id2label_dict[id]  for id in predict_labels if id!=0]

        start = 1
        end = len(original_labels) -1  # 当 len(original_labels) -1 > 1的时候,只要有一个字就没问题
        original_labels = original_labels[start:end] ##去除首尾的token
        predict_labels = predict_labels[start:end]
        #print(predict_labels)
        #print(original_labels)
        def merge(labelList):
            new_label = []
            chars = ""
            for i, label in enumerate(labelList):
                if label not in ("b", "m", "e", "s"):  # 可能是其他标签
                    if len(chars) != 0:
                        new_label.append(chars)
                    new_label.append(label)
                    chars = ""
                elif label == "b":
                    if len(chars) != 0:
                        new_label.append(chars)
                    chars = "b"
                elif label == "m":
                    chars += "m"
                elif label == "s":
                    if len(chars) != 0:
                        new_label.append(chars)
                    new_label.append("s")
                    chars = ""
                else:
                    new_label.append(chars + "e")
                    chars = ""
            if len(chars) != 0:
                new_label.append(chars)
            orderList = []
            start = 0
            end = 0
            for each in new_label:
                if each == "[CLS]" or each == "[SEP]":
                    end = start + 1
                else:
                    end = start+len(each)
                orderList.append((start, end))
                start = end
            assert end == len(labelList)
            return orderList
        right = merge(original_labels)
        predict = merge(predict_labels)
        return right, predict,original_labels,predict_labels




if __name__ == "__main__":
    #import pickle
    #with open('./output/label2id.pkl', 'rb') as rf:
    #    label2id = pickle.load(rf)
    #    id2label = {value: key for key, value in label2id.items()}
    #    print(id2label)
    id2label={1:"s",
      2:"b",
      3:"m",
      4:"e",
      5:"X",
      6:"[CLS]",
      7:"[SEP]"
    }

    e = SegmenterEvaluation(id2label)
    precision, recall, f1, error, right, predict = e.evaluate([6, 1, 1, 2, 3, 4, 7, 0, 0, 0], [6, 2, 4, 2, 3, 6, 7, 0, 0, 0])
    print(precision, recall, f1, error)

