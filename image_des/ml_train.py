from libsvm.python.svmutil import *
from libsvm.python.svm import *


y, x = svm_read_problem('result.txt')
model = svm_train(y, x)
svm_save_model('d.py', model)

#print(svm_root)

# yt, xt = svm_read_problem('6 1:7 2:3 3:3 4:3 5:3 6:4 7:3 8:1 9:1 10:1 11:5 12:2 13:2 14:2 15:2 16:4')
# print(yt)
# model = svm_load_model('d.py')
# p_label, p_acc, p_val = svm_predict(yt, xt, model)
# print('!!!!!!!!!!!!')
# print(p_label[0])
#print(p_acc)
#print(p_val)