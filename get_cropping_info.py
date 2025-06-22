import requests
import pandas as pd
import json
from config import SERVICE_KEY

# 필수 정보
USER_IDS_JSON = "smartfarm_data.json"  # 농가정보 파일명

# userId 목록 불러오기
with open(USER_IDS_JSON, "r", encoding="utf-8") as f:
    user_ids = [item["userId"] for item in json.load(f)]

# 작기정보 요청 함수
def get_cropping_season(service_key, user_id):
    url = f"http://www.smartfarmkorea.net/Agree_WS/webservices/ProvideRestService/getCroppingSeasonDataList/{service_key}/{user_id}"
    try:
        r = requests.get(url, verify=False)  # SSL 인증서 검증 비활성화
        if r.status_code == 200:
            try:
                data = r.json()
                # statusCode가 "00"인 정상 데이터만 추출
                data = [row for row in data if row.get("statusCode") == "00"]
                # userId 추가(누락 대비)
                for row in data:
                    row["userId"] = user_id
                return data
            except Exception as e:
                print(f"JSON 파싱 오류: {e}, {r.text}")
                return []
        else:
            print(f"요청 실패: {user_id}, status: {r.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"요청 중 오류 발생: {e}")
        return []

# 전체 userId에 대해 요청
all_cropping = []
for user_id in user_ids:
    print(f"\n{user_id} 농가의 작기정보를 조회합니다...")
    data = get_cropping_season(SERVICE_KEY, user_id)
    if data:
        all_cropping.extend(data)
        print(f"- {len(data)}개의 작기정보가 조회되었습니다.")

# 데이터프레임으로 정리 및 저장
if all_cropping:
    df = pd.DataFrame(all_cropping)
    print("\n=== 데이터 미리보기 ===")
    print(df.head())
    
    # 실제 데이터의 컬럼명 확인
    print("\n=== 사용 가능한 컬럼 목록 ===")
    print(df.columns.tolist())
    
    # 필수 컬럼만 선택 (실제 데이터에 있는 컬럼명으로 수정)
    cols = ['userId', 'statusCode', 'statusMessage', 'croppingSerlNo', 'itemCode', 'croppingSeasonName', 'croppingDate', 'croppingEndDate']
    
    # 선택한 컬럼이 모두 존재하는지 확인
    available_cols = [col for col in cols if col in df.columns]
    if len(available_cols) != len(cols):
        print("\n경고: 일부 컬럼이 데이터에 존재하지 않습니다.")
        print("존재하지 않는 컬럼:", set(cols) - set(available_cols))
        print("사용 가능한 컬럼으로 저장을 진행합니다.")
        cols = available_cols
    
    # CSV 파일로 저장
    df[cols].to_csv("cropping_info.csv", index=False, encoding="utf-8-sig")
    print("\n작기정보가 cropping_info.csv 파일로 저장되었습니다.")
    
    # 전체 데이터를 JSON 파일로도 저장
    with open('cropping_info.json', 'w', encoding='utf-8') as f:
        json.dump(all_cropping, f, ensure_ascii=False, indent=2)
    print("작기정보가 cropping_info.json 파일로도 저장되었습니다.")
else:
    print("\n조회된 작기정보가 없습니다.")