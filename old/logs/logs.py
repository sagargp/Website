import GeoIP as G
def index(req):
  import ApacheLogParser as A
  import cgi

  userAgentBlacklist = ["bot", "spider"]
  refererBlacklist   = ["sagarpandya.com"]
  responseBlacklist  = ["404"]
  requestBlacklist   = ["robots.txt", "favicon"]

  geo = G.open('GeoLiteCity.dat', G.GEOIP_STANDARD)
  log = open('data.log')

  domains = {}
  for line in log.read().splitlines():
    # city, region_name, country_name, postal_code
    # date
    # request
    # referrer
    # user_agent
    logline = A.ApacheAccessLogParser()
    logline.parse(line)

    userAgent = logline.user_agent.lower()
    referer   = logline.referer.lower()
    request   = logline.request.lower()
    response  = logline.response.lower()

    skip = False
    for x in userAgentBlacklist:
      if x in userAgent:
        skip = True

    for x in refererBlacklist:
      if x in referer:
        skip = True

    for x in responseBlacklist:
      if x in response:
        skip = True

    for x in requestBlacklist:
      if x in request:
        skip = True

    if skip:
      continue

    referringDomain = referer.replace('http://', '').replace('https://', '').split('/')
    referringDomain = referringDomain[0]

    record = geo.record_by_addr(logline.ip_address)

    marker = '<marker ip="%s" lat="%s" lng="%s" city="%s" region="%s" country="%s" postal="%s" date="%s" request="%s" referer="%s" useragent="%s"/>' % (
      cgi.escape("%s" % logline.ip_address, quote=True),
      cgi.escape("%s" % record['latitude'], quote=True),
      cgi.escape("%s" % record['longitude'], quote=True),
      cgi.escape("%s" % record['city'], quote=True),
      cgi.escape("%s" % record['region_name'], quote=True),
      cgi.escape("%s" % record['country_name'], quote=True),
      cgi.escape("%s" % record['postal_code'], quote=True),
      cgi.escape("%s" % logline.date, quote=True),
      cgi.escape("%s" % logline.request, quote=True),
      cgi.escape("%s" % logline.referer, quote=True),
      cgi.escape("%s" % logline.user_agent, quote=True)
    )
    
    marker = marker.decode("windows-1251", "ignore").encode("ascii", "ignore")
    
    if domains.has_key(referringDomain):
      domains[referringDomain].append(marker)
    else:
      domains[referringDomain] = [marker]

  data = ["<?xml version=\"1.0\" encoding=\"UTF-8\" ?>", "<markers>"]
  for domain in domains.keys():
    data.append('<domain name="%s">' % domain.replace('"', ''))
    for marker in domains[domain]:
      data.append(marker)
    data.append('</domain>')
  data.append('</markers>')
  return '\n'.join(data)

if __name__ == '__main__':
  print index(None)
