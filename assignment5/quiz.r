setwd("C:/Users/wwebb/Dropbox/GitHub/datasci_course_materials/assignment5")
om=read.csv("seaflow_21min.csv") 

str(om)

# Question 1
sum(om$pop=="synecho")

# Question 2
summary(om$fsc_small)
quantile(om$fsc_small)

# Question 3
set.seed(100)
test_subscript=sample(nrow(om),nrow(om)/2)
om_test=om[test_subscript,]
om_train=om[-test_subscript,]

mean(om_train$time)

# Question 4
library(ggplot2)
ggplot(aes(x=chl_small,y=pe,color=pop),data=om)+geom_jitter()

# Question 5, 6, 7
library(rpart)
library(rpart.plot)
fol <-formula(pop~fsc_small + fsc_perp + chl_small + pe + chl_big + chl_small)
model_1<-rpart(fol,method="class",data=om_train)
print(model_1)

# Question 8
om_predict_1=predict(model_1,newdata=om_test)
pop_test_1=c()
pop_names=c("crypto","nano","pico","synecho","ultra")
for (i in 1:nrow(om_predict_1)){
        pop_test_1=c(pop_test_1,pop_names[which.max(om_predict_1[i,])])
        } 
result_1=as.vector(om_test$pop)==pop_test_1
table(result_1)
accuracy_1=sum(result_1)/length(pop_test_1)
accuracy_1

## Question 9
library(randomForest)
model_2 <- randomForest(fol, data=om_train)
plot(model_2)

om_predict_2=predict(model_2,type="prob",newdata=om_test)
pop_test_2=c()
for (i in 1:nrow(om_predict_2)){
        pop_test_2=c(pop_test_2,pop_names[which.max(om_predict_2[i,])])
        } 
result_2=as.vector(om_test$pop)==pop_test_2
table(result_2)
accuracy_2=sum(result_2)/length(pop_test_2)
accuracy_2

# Question 10
importance(model_2)

# Question 11, 12
library(e1071)
model_3 <- svm(fol, data=om_train)
om_predict_3=predict(model_3,newdata=om_test)
table(pred = om_predict_3, true =om_test$pop)


# Question 13
qplot(fsc_big,data=om)

# Question 14
om_clean=om[om$file_id!=208,]
set.seed(100)
test_subscript2=sample(nrow(om_clean),nrow(om_clean)/2)
om_clean_test=om_clean[test_subscript2,]
om_clean_train=om_clean[-test_subscript2,]
model_4 <- svm(fol, data=om_clean_train)
om_clean_predict_4=predict(model_4,newdata=om_clean_test)
table(pred = om_clean_predict_4, true =om_clean_test$pop)
