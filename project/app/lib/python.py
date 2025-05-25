from supabase import create_client, Client

# Supabase URL ve API anahtarını buraya koy
url = "https://db.wtshmlzydzybuvnbjcet.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind0c2htbHp5ZHp5YnV2bmJqY2V0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDgxMjU2NDYsImV4cCI6MjA2MzcwMTY0Nn0.rEStv_UaXStp3Hr0S7X8zkIT72lNnRx7WsZjScuTfDc"  # Buraya API anahtarını eklemelisin

supabase: Client = create_client(url, key)

# Veritabanından veri almak
data = supabase.table('your_table_name').select('*').execute()

print(data)
