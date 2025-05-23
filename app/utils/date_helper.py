from datetime import datetime, timedelta

def generate_dates():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    return [
        f"{d.day}-{d.month}-{d.year}"
        for d in (start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1))
    ]

def get_day_name(date_obj: datetime):
    days = ["Chủ Nhật", "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy"]
    return days[date_obj.weekday()]
