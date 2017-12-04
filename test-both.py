import lda_try
import LDA
import matplotlib.pyplot as plt
import numpy as np

def main(n_iter = 4000, n_topic = 5, n_top_words = 15):
    lda_try.lda_running(n_passes = int(n_iter/50), n_topics = n_topic, n_words = n_top_words)
    LDA.main(n_iter = n_iter, n_topic = n_topic, n_top_words = n_top_words)
    
    
a= [[71,26],[145,52],[285,102],[554,193],[153,97],[306,191],[599,363],[544,166],[7520,6421]]
c= np.array([71,26,145,52,285,102,554,193,153,97,306,191,599,363,544,166,7520,6421])
c = c.reshape((9,2))
b = [1000,2000,4000,8000]
plt.figure(1)

plt.plot(b,c[:4,1],color='deepskyblue',label='no-gensis 5 topics')
plt.plot(b,c[:4,0],color='orange', label='gensis 5 topics')
plt.plot(b[:2],c[4:6,1],color='navy',label='no-gensis 15 topics')
plt.plot(b[:2],c[4:6,0],color='red', label='gensis 15 topics')

plt.plot([2000,2700],[306,413],ls='--',color='gray')
plt.plot([2000,4300],[191,407],ls='--',color='gray')

legend = plt.legend(loc='upper center', shadow=True)
plt.xlabel('n_iter')
plt.ylabel('seconds')
plt.title('Plot of running time vs n_iter\n20 racist books')
plt.show()

plt.figure(2)

plt.plot([15,5],c[6:8,1],color='deepskyblue',label='no-gensis')
plt.plot([15,5],c[6:8,0],color='orange', label='gensis')

legend = plt.legend(loc='upper center', shadow=True)
plt.xlabel('n_topics')
plt.ylabel('seconds')
plt.title('Plot of n_topics vs time \n60 racist books, 2000 iters')
plt.show()

plt.figure(3)

plt.plot([15,5],[97,52],color='deepskyblue',label='no-gensis')
plt.plot([15,5],[153,145],color='orange', label='gensis')

legend = plt.legend(loc='upper center', shadow=True)
plt.xlabel('n_topics')
plt.ylabel('seconds')
plt.title('Plot of n_topics vs time \n20 racist books, 2000 iters')
plt.show()

plt.figure(4)

plt.plot([20,60],c[[1,7],1],color='deepskyblue',label='no-gensis 5 topics')
plt.plot([20,60],c[[1,7],0],color='orange', label='gensis 5 topics')
plt.plot([20,60],c[[4,6],1],color='navy',label='no-gensis 15 topics')
plt.plot([20,60],c[[4,6],0],color='red', label='gensis 15 topics')

legend = plt.legend(loc='upper center', shadow=True)
plt.xlabel('n_doc')
plt.ylabel('seconds')
plt.title('Plot of running time vs n_doc\n2000 iters')
plt.show()

