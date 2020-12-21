import pygsheets

gc = pygsheets.authorize(service_account_file='./test-9db5da40b6b4.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1FwGHUxmmWP_cx4TET16EDhwkvanvMZTFIXNjc8j4bfg')

# read all
wks_read = sh[0]
data = wks_read.get_all_records()
print(data[0])

# write line
test_data = ['test', 23, 1]
wks_write = sh[1]
wks_write.append_table(test_data, start='A2')