# Python wrapper for the [YOAS (Your Own Anti-Spam System) API](https://github.com/yourusername/YOAS-API)  
Little project for managing spam-related text and comments.

You can check this API at https://yourdomain.com/apis/yoas/docs
## How to use
Just use pip: `pip install yoas_api_wrapper`
## Example
```python
from yoas_api_wrapper import YOASAPIWrapperLatest

api_server = "https://pashok11.tw1.su/apis/yoas"
api = YOASAPIWrapperLatest(api_server)

usr = api.get_user(12345678)
if usr.found:
    print(usr.user)
```