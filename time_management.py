import datetime

def current_date_time(*args, **kwargs):
  # Print the received arguments
  print("Positional arguments:", args)
  print("Keyword arguments:", kwargs)
  utc_now = datetime.datetime.now()
  utc_info = "Current UTC date and time: " + str(utc_now)
  print(utc_info)

  return utc_info