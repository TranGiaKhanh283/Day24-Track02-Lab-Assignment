# src/quality/validation.py
import pandas as pd
import great_expectations as gx
from great_expectations.core.expectation_suite import ExpectationSuite

def build_patient_expectation_suite() -> ExpectationSuite:
    """
    Tạo expectation suite cho anonymized patient data.
    """
    context = gx.get_context()
    
    # Lấy validator (GX 1.x style)
    df = pd.read_csv("data/raw/patients_raw.csv")
    ds = context.data_sources.add_pandas(name="my_pandas_datasource")
    asset = ds.add_dataframe_asset(name="my_df_asset")
    validator = asset.get_validator(dataframe=df)



    # --- TASK: Thêm các expectations ---

    # 1. patient_id không được null
    validator.expect_column_values_to_not_be_null("patient_id")

    # 2. cccd phải có đúng 12 ký tự
    validator.expect_column_value_lengths_to_equal(
        column="cccd",
        value=12
    )

    # 3. ket_qua_xet_nghiem phải trong khoảng [0, 50]
    validator.expect_column_values_to_be_between(
        column="ket_qua_xet_nghiem",
        min_value=0,
        max_value=50
    )

    # 4. benh phải thuộc danh sách hợp lệ
    valid_conditions = ["Tiểu đường", "Huyết áp cao", "Tim mạch", "Khỏe mạnh"]
    validator.expect_column_values_to_be_in_set(
        column="benh",
        value_set=valid_conditions
    )

    # 5. email phải match regex pattern
    validator.expect_column_values_to_match_regex(
        column="email",
        regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    )

    # 6. Không được có duplicate patient_id
    validator.expect_column_values_to_be_unique(column="patient_id")

    return validator



def validate_anonymized_data(filepath: str) -> dict:
    """
    Validate anonymized data.
    Trả về dict: {"success": bool, "failed_checks": list, "stats": dict}
    """
    df = pd.read_csv(filepath)
    results = {
        "success": True,
        "failed_checks": [],
        "stats": {
            "total_rows": len(df),
            "columns": list(df.columns)
        }
    }

    # Check 1: Không có null values trong các cột quan trọng
    important_cols = ["patient_id", "ho_ten", "cccd", "email"]
    null_counts = df[important_cols].isnull().sum()
    if null_counts.any():
        results["success"] = False
        results["failed_checks"].append(f"Null values found: {null_counts.to_dict()}")

    # Check 2: CCCD phải được ẩn danh (ví dụ: không còn trong raw data nếu so sánh - nhưng ở đây ta check format hoặc uniqueness)
    # Một cách check đơn giản là check xem có dòng nào CCCD không phải string 12 số không (nếu ta dùng mask thì nó sẽ là string có *)
    # Nếu ta dùng replace, nó vẫn là 12 số.
    
    return results

