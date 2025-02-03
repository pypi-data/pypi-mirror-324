import os
from ardent import ArdentClient, ArdentError
from dotenv import load_dotenv

load_dotenv()

def test_create_and_execute():
    """Test the combined create and execute job workflow"""
    print("Starting integration test...")
    
    client = ArdentClient(
        public_key=os.getenv("PUBLIC_KEY"), 
        secret_key=os.getenv("SECRET_KEY"),
        base_url=os.getenv("BASE_URL"),
        )
    try:




        result = client.create_and_execute_job(
            message="Create a file that prints hello world then runs it",
        )




    except ArdentError as e:
        print(f"Ardent error occurred: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    test_create_and_execute()