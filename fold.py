# 使用scikit-learn内置的乳腺癌数据集
from sklearn.datasets import load_breast_cancer
data = load_breast_cancer()
X,y = data.data,data.target

# 标准化数据并划分训练集与测试集
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)


#K交叉验证
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
model = SVC(kernel='linear')
cvs = [5, 10]
for i in cvs:
    scores = cross_val_score(model,X_train, y_train,cv=i,scoring='accuracy')
    print(f"cv={i}交叉验证平均准确率：{scores.mean():.2f} (±{scores.std():.2f})")


#分层交叉验证
from sklearn.model_selection import StratifiedKFold
stratified_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X_train, y_train, cv=stratified_cv)
print(f"分层交叉验证平均准确率：{scores.mean():.2f}")


# 使用网格搜索选择SVM最优参数
from sklearn.model_selection import GridSearchCV
param_grid = { 'C': [0.1, 1, 10], 'gamma': [0.01, 0.1, 1], 'kernel': ['rbf', 'linear'] }
grid_search = GridSearchCV(SVC(), param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)
print("最优参数组合：", grid_search.best_params_)
print("最优模型验证准确率：", grid_search.best_score_)


# 在独立测试集上验证最优模型性能
# best_model = grid_search.best_estimator_
# y_pred = best_model.predict(X_test)
# print(f"测试集准确率：{accuracy_score(y_test, y_pred):.2f}")


from sklearn.ensemble import RandomForestClassifier
rf_param_grid = {
    'n_estimators' : [50, 100],
    'max_depth':[5,10]
}
rf_model = RandomForestClassifier(random_state=42)
rf_grid_search = GridSearchCV(rf_model, rf_param_grid, cv=5, scoring='accuracy')
rf_grid_search.fit(X_train, y_train)
print("最优参数组合：", rf_grid_search.best_params_)
print("准确率：", rf_grid_search.best_score_)


# 可视化分析：绘制不同k值下交叉验证准确率的分布箱线图
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import cross_val_score

# 收集交叉验证结果（你应该已经有了 cvs 和 model）
cv_scores_dict = {}
for k in cvs:
    scores = cross_val_score(model, X_train, y_train, cv=k, scoring='accuracy')
    cv_scores_dict[f"{k}-fold"] = scores

# 转换为 DataFrame
score_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in cv_scores_dict.items()]))

# 画箱线图（matplotlib）
plt.figure(figsize=(8, 6))
plt.boxplot([score_df[col].dropna() for col in score_df.columns], labels=score_df.columns)
plt.title(f"不同 K 值下交叉验证准确率分布")
plt.ylabel(f"准确率")
plt.xlabel(f"交叉验证折数")
plt.grid(True)
plt.show()


