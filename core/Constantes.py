import string

encoded_name_insta = "Fe\u00cc\u0081lix Fro\u00cc\u00b6ment" 
my_name_insta = "Fe\u00cc\u0081lix Fro\u00cc\u00b6ment".encode('latin-1').decode('utf-8')

encoded_name_fb = "F\u00c3\u00a9lix Froment"
my_name_fb = "F\u00c3\u00a9lix Froment".encode('latin-1').decode('utf-8')