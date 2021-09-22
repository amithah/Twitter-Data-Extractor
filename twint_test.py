import twint

c = twint.Config()

c.Username = "noneprivacy"
c.Custom["tweet"] = ["id"]
c.Custom["user"] = ["bio"]
c.Limit = 10
c.Store_csv = True
c.Output = "none"

twint.run.Search(c)
