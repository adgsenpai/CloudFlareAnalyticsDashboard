#ADGSTUDIOS - server.py

from flask import Flask,render_template,send_from_directory
import gqlcloudflare as gql

app = Flask(__name__,template_folder='./pages')

# set your domain name here
domainname = 'mydomain'


# allows for files to be refreshed in server
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
  gql.RetriveWebAnalytics()
  return render_template('index.html',
  domainname=domainname,
  total_data_transfered_today=str(gql.GetTotalDataServedToday()) + " GB", 
  total_requests_today=gql.GetTotalRequestsToday(), 
  total_page_views_today=gql.GetTotalPageViewsToday(),
  total_devices_today=gql.GetUniqueDevicesToday(),
  AnalyticsDF = gql.GetAnalyticsDF().to_dict(),
  BroswerData = gql.GetBroswerDataDF().to_dict()['pageViews'],
  CountryData = gql.GetCountryData().to_dict()
  )

@app.route('/dashboard-free.css.map')
def cssmap():
  return send_from_directory('./static/css','dashboard-free.css.map')

#running server on port 8000 - you can change the values here
if __name__ == "__main__":
  app.run(host="0.0.0.0",port=8000)