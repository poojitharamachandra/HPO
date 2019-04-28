learning_rates=[]
batch_sizes=[]
accuracies=[]
i=0
data_file= open("data_file.txt","r")
for line in data_file:
    if "[" in line:
        chunks=line.split(",")
        learning_rates.append(float(chunks[1]))
        batch_sizes.append(int(chunks[2]))
        accuracies.append(int(chunks[3]))
        i+=1       

idx_32=[]
idx_64=[]
idx_128=[]
idx_256=[]

for i in range(0,len(batch_sizes)):
    if batch_sizes[i]== 32 :
        idx_32.append(int(i))
    if batch_sizes[i]== 64 :
        idx_64.append(int(i))
    if batch_sizes[i]== 128 :
        idx_128.append(int(i))
    if batch_sizes[i]== 256 :
        idx_256.append(int(i))

import matplotlib.pyplot as plt
plt.scatter(np.array(learning_rates)[idx_32],np.array(accuracies)[idx_32],c="r",label="batch size=32")
plt.scatter(np.array(learning_rates)[idx_64],np.array(accuracies)[idx_64],c="b",label="batch size=64")
plt.scatter(np.array(learning_rates)[idx_128],np.array(accuracies)[idx_128],c="y",label="batch size=128")
plt.scatter(np.array(learning_rates)[idx_256],np.array(accuracies)[idx_256],c="g",label="batch size=256")
#plt.plot(accuracies)
plt.legend(loc=1)
plt.xlabel("Learning_Rate")
plt.ylabel("Accuracy")
plt.xlim(0,0.1)
plt.title("Accuracies for different Configurations")
plt.show()

plt.xlabel("No. of epochs")
plt.ylabel("Loss")
plt.ylim(0,2)
plt.plot(progress)
plt.show()



