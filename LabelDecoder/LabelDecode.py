from sklearn.preprocessing import LabelEncoder  
from numpy._distributor_init import NUMPY_MK
le = LabelEncoder()
le.fit_transform(["paris", "paris", "tokyo", "amsterdam"])
print(list(le.classes_))