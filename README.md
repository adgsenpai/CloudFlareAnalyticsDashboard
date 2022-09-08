<img src="https://upload.wikimedia.org/wikipedia/commons/1/17/GraphQL_Logo.svg" width="200" height="200" align="right" />

<img src="https://upload.wikimedia.org/wikipedia/commons/9/94/Cloudflare_Logo.png" width="150" height="150" align="right" />


# Cloudflare Analytics Dashboard Tool

This is a tool to help you get started with Cloudflare Analytics. It uses the GraphQL API to fetch data from Cloudflare and display it in a dashboard. You may use this tool to get started with Cloudflare Analytics, or as a reference for how to use the GraphQL API.

## Getting Started

In `app.py` set the following variables:

```
domainname = 'mydomain'
```

In `gqlcloudflare.py` set the following variables:

```
#FULL IN YOUR CLOUDFLARE DETAILS HERE
gqlapikey = 'APIKEY'
email = 'EMAIL'
zonetag = 'ZONEID'
```

Once done, run the following command to install the required packages:

```
pip install -r requirements.txt
```

Then run the following command to start the dashboard:

```
python app.py
```

## Deployment to Web

This tool is deployed using Heroku. You can deploy it using Heroku by clicking the button below:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Click the button above, and then fill in the required details.

Set the app type to `Container Type` using the Heroku CLI:

Then `Deploy App`.

Once the app is deployed, click the `Manage App` button. Then click the `Open App` button to open the app.


## Screenshots
![Screenshot 1](./static/adgstudios.co.za.png)

### Made with ❤️ by [ADGSTUDIOS](https://adgstudios.co.za)

