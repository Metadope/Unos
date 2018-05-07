#kbAsciiMaroo.py - Windows-specific Ascii Chart Dilemma
import msvcrt, time, sys, random, colorama

#Globals
out = sys.stderr
c = "."
maxc = count = 64
chars = score = 0
colormyline = ""
myline = ""
thisline = ""
cheat = 0
decr = 4
sleeper = 0.1
nog = chr(7) + chr(8) + chr(9) + chr(10) + chr(13)
special = chr(1) + chr(2) + chr(27)
#my command prompt uses Deja Vu Sans Mono, with DOS:United States - your glyphs may differ
bonus3 = chr(27) 
bonus2 = chr(15) + chr(14) #cog & music (NO)
bonus = chr(1) + chr(2) +  chr(3) + chr(4) +  chr(5) + chr(6)

def AsciiChart():
  #global out,nog
  out.write("  : 0 1 2 3 4 5 6 7 8 9 A B C D E F 0 1 2 3 4 5 6 7 8 9 A B C D E F\n")
  for j in range( 0, 8):
    out.write("%02x:" % j)
    for i in range(0,32):
      ij = chr(i + 32 * j)
      if ij in nog:
        ij = '-'
      out.write(" %s" % ij)
    out.write("\n")

def Yellow(pstr):
  return colorama.Fore.YELLOW + pstr + colorama.Fore.RESET
def Green(pstr):
  return colorama.Fore.GREEN + pstr + colorama.Fore.RESET
def Red(pstr):
  return colorama.Fore.RED + pstr + colorama.Fore.RESET
def Blue(pstr):
  return colorama.Fore.BLUE + pstr + colorama.Fore.RESET
def White(pstr):
  return colorama.Fore.WHITE + pstr + colorama.Fore.RESET
def Cyan(pstr):
  return colorama.Fore.CYAN + pstr + colorama.Fore.RESET
def Magenta(pstr):
  return colorama.Fore.MAGENTA + pstr + colorama.Fore.RESET
def Black(pstr):
  return colorama.Fore.BLACK + pstr + colorama.Fore.RESET

def Bright(pstr):
  return colorama.Style.BRIGHT + pstr + colorama.Style.NORMAL
  
def BrightGreen(pstr):
  return Bright(Green(pstr))
def BrightYellow(pstr):
  return colorama.Style.BRIGHT + colorama.Fore.YELLOW + pstr + colorama.Style.RESET_ALL

def Score():
  if score > 64:
    result = BrightGreen("\n\nYou WIN! You're the best!\n")
  elif score > 16:
    result = Bright("\n\nYou WIN!\n")
  elif maxc <= 0:
    result = "\n\nYou ran out of time, dude!\n"
  else:  
    result = "\n\nYou didn't win the game, sorry!\n"

  print "\nYou hit %d keys and scored %d points:" % (len(myline), score)
  print "You hit these (winners and losers): " + colormyline + result
  iavg = chars/score
  print "You saw %d characters. It took you an average of %d chars per point." % (chars, iavg)
  if iavg <= 5 and score > 100:
    print Bright(Cyan("Dude! High Score! How'd you do that? Live long and prosper."))
  else:
    print Bright(Cyan("Not a high score, but next time you can cheat!"))
  sys.exit(1)

def StartNewLine(addCR="\n"):
  global thisline, count, maxc, decr, cheat, sleeper
  thisline = ""
  count = 0
  if maxc == 32:
    print Yellow("\n\nTime's ticking: you'd better hurry!")
  elif maxc == 16:
    print BrightYellow("\n\nHurry!")
    decr = 2
    sleeper += 0.1
    cheat = 1
  elif maxc == 8:
    sleeper += 0.1
    cheat = 2
  out.write(addCR + "%02x:%02x: " % (score,maxc))

def GetNewTargetChar():
  global c, nog, chars
  if cheat == 0:
    c = chr(random.randint(0,255))
    if c in nog or c == 0:
      GetNewTargetChar()
  elif cheat == 1:
    c = chr(random.randint(32,127))
  else:
    c = chr(random.randint(64,127))

def ScoreHit( ccc ):
  lscore = 1 #local
  if ccc in bonus:
    lscore += 5
  if ccc in bonus2:
    lscore += 10
  if ccc in bonus3:
    lscore += score #more than doubles your score
  return lscore
  
def Prefilter( ccc ):
    return ccc
    
AsciiChart()
colorama.init()
#print colorama.Style.BRIGHT + "Press a key ('q' to quit):" + colorama.Style.NORMAL
out.write("Score a bonus with any of these characters: %s\n" % bonus);
out.write("A double bonus with any of these characters: %s\n" % bonus2);
out.write("A spectacular bonus with this character: %s\n" % bonus3);

print Bright("Press a key ('q' to quit):")

while True:
  try:
    while not msvcrt.kbhit():
      if count == maxc:
        StartNewLine()
        maxc -= decr
        if maxc <= 0:
          Score()
      time.sleep(sleeper)
      GetNewTargetChar()
      thisline += c
      out.write(c)
      count += 1
      chars += 1
  except KeyboardInterrupt:
    c = chr(3)

  if c != chr(3):
    cc = msvcrt.getch()
  else:
    cc = c
  
  cc = Prefilter( cc ) #for future handling of special keys
  if cc == "q":
    if score < 1:
      score = 1
    print BrightYellow(cc)
    break
  elif cc in thisline: #good
    myline += cc
    if len(thisline) <= 16:
      score += 1
    score += ScoreHit( cc )
    if cc not in special: #chars that will disappear when I send them thru colorama
      cc = Green(cc)
    
    colormyline += cc
    maxc += 2
    if maxc > 64:
      maxc = 64
    print cc
    StartNewLine("")
  else: #bad
    myline += cc
    if cc not in special:
      cc = Red(cc)
    colormyline += cc
    print cc + chr(7)
    maxc -= decr
    score -= 1
    StartNewLine("")
  #out.write(cc)
  while msvcrt.kbhit():
    msvcrt.getch()
Score()
    