import requests
import json
from datetime import datetime
from config import SERVICE_KEY

def get_smartfarm_info(service_key):
    """
    스마트팜 농가정보를 조회하는 함수
    
    Args:
        service_key (str): 스마트팜 코리아 API 서비스 키
    
    Returns:
        list: 농가정보 리스트
    """
    # API 엔드포인트 URL
    url = f"http://www.smartfarmkorea.net/Agree_WS/webservices/ProvideRestService/getIdentityDataList/{service_key}"
    
    try:
        # API 요청
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        
        # JSON 응답 파싱
        data = response.json()
        
        # 결과 출력
        print("\n=== 스마트팜 농가정보 ===")
        print(f"총 {len(data)}개의 농가정보가 조회되었습니다.\n")
        
        for farm in data:
            print(f"농가 ID: {farm.get('userId')}")
            print(f"시설 ID: {farm.get('facilityId')}")
            print(f"주소: {farm.get('addressName')}")
            print(f"품목 코드: {farm.get('itemCode')}")
            print("-" * 50)
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}")
        print("응답 내용:", response.text)
        return None

def save_to_json(data, filename="smartfarm_data.json"):
    """
    농가정보를 JSON 파일로 저장하는 함수
    
    Args:
        data (list): 저장할 농가정보 리스트
        filename (str): 저장할 파일 이름
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n농가정보가 {filename} 파일로 저장되었습니다.")
    except Exception as e:
        print(f"파일 저장 중 오류 발생: {e}")

if __name__ == "__main__":
    # 농가정보 조회
    farm_info = get_smartfarm_info(SERVICE_KEY)
    
    # 농가정보가 성공적으로 조회되었다면 JSON 파일로 저장
    if farm_info:
        save_to_json(farm_info) 