import pandas as pd

# قراءة الملف
data = pd.read_csv("log.csv")

# إزالة الفراغات في أسماء الأعمدة
data.columns = data.columns.str.strip()

# حذف الصفوف المكررة
data = data.drop_duplicates()

# تحويل الأعمدة الرقمية فقط
numeric_cols = ["Iteration", "Throughput(Mbps)", "Latency(ms)"]
for col in numeric_cols:
    data[col] = pd.to_numeric(data[col], errors="coerce")

# تجميع البيانات حسب Iteration وأخذ المتوسط فقط للأعمدة الرقمية
data_clean = data.groupby("Iteration", as_index=False)[numeric_cols[1:]].mean()

# حفظ الملف الجديد
data_clean.to_csv("log_clean.csv", index=False)

print("✅ تم تنظيف الملف بنجاح وحفظه باسم log_clean.csv")
