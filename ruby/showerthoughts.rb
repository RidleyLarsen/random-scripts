require 'unirest'
require 'subprocess'

def harvest_titles jsonobj
    lst = []
    jsonobj["children"].each do |child|
      lst.push(child["data"]["title"])
    end
    return lst
end

def main
    puts "Grabbing shower thoughts."
    base_uri = "https://www.reddit.com/r/showerthoughts/top.json?t=all,limit=100"
    response = Unirest.get base_uri
    db = harvest_titles response.body["data"]
    while db.length < 500
      after = response.body["data"]["children"][-1]["data"]["name"]
      puts "Next: #{after}"
      response = Unirest.get "#{base_uri}&after=#{after}"
      titles = harvest_titles response.body["data"]
      if titles.length < 1
          break
      end
      db += titles
    end
    file = File.open("showerthoughts.txt", "w")
    db.each do |title|
      file.write("#{title}\n%\n")
    end
    file.close unless file.nil?
    puts "Wrote #{db.length} titles to file."
    begin
      Subprocess.check_call(["strfile", "-c", "%", "showerthoughts.txt", "showerthoughts.dat"])
    rescue Subprocess::NonZeroExit => e
      puts "Oops. Had a problem building the fortune file."
      puts e.message
    end
end

main()
