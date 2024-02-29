"""
This code imports the necessary libraries and creates a Typer app. It also defines a class for a JSToFastAPIModule and a function for converting JS source code to FastAPI source code. The code also creates a streamlit component and a router for handling requests to convert JS code to FastAPI code. Finally, the main function initializes the necessary tools and calls the function to convert the provided JS source code to FastAPI code.
"""
import dspy
from typer import Typer

from dspygen.signatures.generate_answer import JSToFastAPISig
from dspygen.utils.dspy_tools import init_dspy


app = Typer()        


class JSToFastAPIModule(dspy.Module):
    """JSToFastAPIModule"""

    def forward(self, js_source):
        pred = dspy.ChainOfThought(JSToFastAPISig)
        result = pred(js_source=js_source).fast_api_source
        return result


def js_to_fast_api_call(js_source):
    js_to_fast_api = JSToFastAPIModule()
    return js_to_fast_api.forward(js_source=js_source)


@app.command()
def call(js_source):
    """JSToFastAPIModule"""
    init_dspy()
    
    print(js_to_fast_api_call(js_source=js_source))


# TODO: Add streamlit component


from fastapi import APIRouter
router = APIRouter()

@router.post("/js_to_fast_api/")
async def js_to_fast_api_route(data: dict):
    # Your code generation logic here
    init_dspy()
    
    print(data)
    return js_to_fast_api_call(**data)


TEST = """function redirectToAuthorization() {
  const authorizationEndpoint = 'https://oauth-provider.com/authorize';
  const clientId = 'your-client-id';
  const redirectUri = 'https://your-app.com/callback';
  const scope = 'desired-scopes';
  const state = 'random-state';

  const redirectUrl = `${authorizationEndpoint}?client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${encodeURIComponent(scope)}&state=${state}`;
  window.location.href = redirectUrl;
}

// Step 5: Exchange authorization code for access token
async function exchangeAuthorizationCode(authorizationCode) {
  const tokenEndpoint = 'https://oauth-provider.com/token';
  const clientId = 'your-client-id';
  const clientSecret = 'your-client-secret';
  const redirectUri = 'https://your-app.com/callback';
  
  const requestBody = {
    grant_type: 'authorization_code',
    code: authorizationCode,
    client_id: clientId,
    client_secret: clientSecret,
    redirect_uri: redirectUri
  };

  const response = await fetch(tokenEndpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody)
  });

  const tokenData = await response.json();
  return tokenData.access_token;
}
"""


def main():
    init_dspy()
    js_source = TEST
    result = js_to_fast_api_call(js_source=js_source)

    with open("fast_code.py", 'w') as f:
        f.write(result)
    

if __name__ == "__main__":
    main()
