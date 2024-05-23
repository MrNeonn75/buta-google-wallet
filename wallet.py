import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/wallet_object.issuer']

class GoogleAPIClient:
    def __init__(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('walletobjects', 'v1', credentials=creds)

    def genericobject(self):
        return self.service.genericobject()

class ClassContainingCreateObjectMethod:
    def __init__(self, client):
        self.client = client
    
    def create_object(self, issuer_id: str, class_suffix: str, object_suffix: str) -> str:
        """Create an object.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for the pass class.
            object_suffix (str): Developer-defined unique ID for the pass object.

        Returns:
            The pass object ID: f"{issuer_id}.{object_suffix}"
        """

        # Check if the object exists
        try:
            self.client.genericobject().get(resourceId=f'{issuer_id}.{object_suffix}').execute()
        except HttpError as e:
            if e.status_code != 404:
                # Something else went wrong...
                print(e.error_details)
                return f'{issuer_id}.{object_suffix}'
        else:
            print(f'Object {issuer_id}.{object_suffix} already exists!')
            return f'{issuer_id}.{object_suffix}'

        # See link below for more information on required properties
        # https://developers.google.com/wallet/generic/rest/v1/genericobject
        new_object = {
            'id': f'{issuer_id}.{object_suffix}',
            'classId': f'{issuer_id}.{class_suffix}',
            'state': 'ACTIVE',
            'heroImage': {
                'sourceUri': {
                    "uri": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxAHDRAOEBAQEBAKEBINDRUNDRAQEA8RIBYWFiAWHxckKCosJCAxHxoYIT0kJjUtOi8xFx8/ODMsQygtOisBCgoKDQ0OGhAQGyslHyUrNy0uLSstLS0rLSstLS0tLSsrLS0tKys3LSstLTc3LSstLi03LSsrKzctNy03Ny0tK//AABEIAMgAyAMBIgACEQEDEQH/xAAcAAEAAgMBAQEAAAAAAAAAAAAABgcBBAUCAwj/xAA8EAACAgADBQMICAUFAAAAAAAAAQIDBAURBgcSITETQWEUIlFxgaGx0RUjMlKRosHwJEJDcoIzU2KS4f/EABoBAQADAQEBAAAAAAAAAAAAAAABAgMFBAb/xAAhEQEAAgIDAQACAwAAAAAAAAAAAQIDEQQSMSFBYRMUMv/aAAwDAQACEQMRAD8AhwAPomIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEB0sLkOLxdDxFdEp1Q11lBxklp179Tmlp7mMa5QxOHb14HG2K9Gvms9bwdhFapYzCQ0ktZ3VwXKXe5JenwPH/Z1kmlltfFVAA9kSgAAQAAAAAAAAAAAAAAAAAAAAAAAAAACxNzEW8ViX3djFfmZbuhWm5jBuNOIvf9SUa4+xav4llnE5U7yy1r4p7edsp9H2PG0R0puelqj0rm+/1P4lflzb3sf5PgI0p88XYl/ivOf6FMvmdHh2m2P6pPoAD1KgAAAAAAAAAAAAAAAAAAAAAAABmEXY1GK1c3wxS6tvly/feYLE3W7LvF2LH2x+rpf8Omvtz6cXsM82SMddymI+rF2Syn6FwNOH/mhHW3xm+b/fgdgwloebJKKbb0SWr8EcKZm07aeKa3u5j5TmEaE/NwlaT/ufP5EGN7PMc8yxd+If9eyU4/268vdoaJ3MNetIhnP2QAGqAAAAAAAAAAAAAAAAAAAAASkMpa9Orei016nqmmV8owhFynY1GEYrVyZcmw+wteSqN96jPEyWqWicafBePiYZs9ccftMRtH9jd3MsTw342LjDXijS+Tl3+d6PUWtRTGiKjFKMYpKKiklFehIw7Y19Wlr6WkfVPU4+TLa87leI0Ed2+zH6OyzET10lZDsYeuXm/DVkiIlvHyO/PcJGujRyqn2ji5KKnyaK49d434KLBL793OYU0u1xg3FOXBGac9OpEDu0yUt/mds5AAXQAAAAAAAAAAAAAAAAAAAASLYPJPpzH11yWtVP112vRpaaR9rK3vFKzaUpxur2ahh6ljrEpWXL6lcn2cPmyw5vRNrm9OXicbEbJ4OyTnCrsLH/AD4ScqJflPl9EY3Dcqcc5R6JYumNjX+S0b9pw73727TLSI05+zWSYbOcHDF4mqGJux0XZZK6PG49VwR1+yl00Rv7Ka4e3F4VTlOnBWQjS5ScnWnHidevgLcsuyrK7acNJzxHDOxS0ScrJS4pNLu6vT2GvkGcZfllccOpvDSb4pxxilVZKb6tuXJvxTIn7CUrfIqTazeBisHmM68PKKqwk+zlGUE+0a66v3FnZhj4YTDWYjVONNcrNU009E2fm662V0pTk9ZWSc5N/ebbZ6eHhi8zNo+K2nS357z8IsN2ijZ23D/p8L04v7vQU/ZJzk2+sm2/X1PIOjiwUxb6q+gANVQAAAAAAAAAAAAAAAAAAC2tzWCUMNfiH1ts7NepJfP3FSl3bp0llUPG2zU8fNtrGtX1MwDLOS0Y0PlfhoYiPDZCM4vqpxUl+DNTNs1ryqCnPibnLgrhXFyssn91I0cNtGu1hVfRdhne+GmVyi4WS+7xJvR+BMRP4HC2r2Zwtapoog6JZhfGqSoslCDr5yk3DXTovQcbMd1D5vD4jXvUbofqiYuXl2bpdY5bRq/Cyb+Oi95IkaxmvTWpRMRL8+Z7sljMjjx3VfVp6ccJKUUcLUsDern9t+KlgYvhppUXNL+ebWvP99xx93NNOKzKFV9UbY3QmoqcU4qWmuun76nUx5bRi73Un1FwXhmW7jL8Zq4wlS331Ten4PUgO2Wwr2cp7dX9pBzVejhpLnqRj5eO868OsoaAD0qgAAAAAAAAAAAAAAABb+5zFqzB20686LeL2SS+RUBLt2ecrKswjCb0rxi7KWvRS5cL/H4nn5VO2OVq+rzA11MnEaIztJPyHFYTGTjKVGG7SFrjFy7FySSsa9Hdr4nnM9osrxtcqrbq7oTWs1WpWqC+83Febp115Ena1OHtVZHAZfiHCMVK2DqglFLisn5i97LxMTobmTZbRltelEUo2/WOXE5uzVdXJ82dE1MrwvkOHpp1b8nqhVq+/SKRtlZ9EN2x2Er2is7eNjpu0UZPh1jZHxR52O2Fhs9Y75Wdrc4uEWo8MYJ9dETQwafzX69d/EagK43y4tRw1FK62WOb9SX/AKWPqURvHzlZvmM1F614P6mDXRtdff8AA14tO2SP0i3iKgA7LMAAAAAAAAAAAAAAAAHt5+AASvDd5tUs8w6qsl/E4daTT62R6cXzJifmXA4yzAWwuqk4TqfFBpvl3FxbI7wKM2UasQ40X9POaULPFP8AQ5PJ401mZr4vWycMju0L8rxmBwq6dq8XYv8AjBcvzNfgSHiI9lS8szPF392FjXhIev7cvivwPJVZIkZPKZnUgZMamHLT2EG2v3g05WpU4Zxuv5ptPWuvu5vv9SLUpa86iEb0+u8XapZLQ6KpfxGIjpHTTWqP3vkUm+Z9sZi7MbZK22TnZY+KUn1Z8Ts8fDGKNKTOwAG6oAAAAAAAAAAAAAAAAAABnX3+owAOtlu0uNytJU4myMV0jJqcF7H09h2cr3hYvLlKMYUNWTlbPWDTlN82+pEAZWwUt7CdysFb18V/sUf9pGrid5+Pt+xGmHqg5fqQgFY42KPwbdjM9qcdmicbcTY4y6xi1CL9aXX2nHQBtWlax8hHoACQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB/9k="
                },
                'contentDescription': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Buta Grup'
                    }
                }
            },
            'textModulesData': [{
                'header': 'Nariman Aliyev',
                'body': 'Software Engineer',
                'id': 'TEXT_MODULE_ID'
            }],
            'linksModuleData': {
                'uris': [{
                    'uri': 'http://maps.google.com/',
                    'description': 'Link module URI description',
                    'id': 'LINK_MODULE_URI_ID'
                }, {
                    'uri': 'tel:6505555555',
                    'description': 'Link module tel description',
                    'id': 'LINK_MODULE_TEL_ID'
                }]
            },
            'imageModulesData': [{
                'mainImage': {
                    'sourceUri': {
                        'uri': 'http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg'
                    },
                    'contentDescription': {
                        'defaultValue': {
                            'language': 'en-US',
                            'value': 'Image module description'
                        }
                    }
                },
                'id': 'IMAGE_MODULE_ID'
            }],
            'barcode': {
                'type': 'QR_CODE',
                'value': 'QR code'
            },
            'cardTitle': {
                'defaultValue': {
                    'language': 'en-US',
                    'value': 'Generic card title'
                }
            },
            'header': {
                'defaultValue': {
                    'language': 'en-US',
                    'value': 'Generic header'
                }
            },
            'hexBackgroundColor': '#4285f4',
            'logo': {
                'sourceUri': {
                    'uri': 'https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/pass_google_logo.jpg'
                },
                'contentDescription': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Generic card logo'
                    }
                }
            }
        }

        # Create the object
        response = self.client.genericobject().insert(body=new_object).execute()

        print('Object insert response')
        print(response)

        return f'{issuer_id}.{object_suffix}'

# Usage example
if __name__ == '__main__':
    client = GoogleAPIClient()
    obj = ClassContainingCreateObjectMethod(client)
    object_id = obj.create_object(issuer_id="your_issuer_id", class_suffix="your_class_suffix", object_suffix="your_object_suffix")
    print("Created object ID:", object_id)
