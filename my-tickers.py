# 08/01/2019 ATOM
# python my-tickers.py <input file>
import urllib.request, urllib.error
import sys
import errno, os
"""Retrieves stock information for given symbols from finance.yahoo.com.
   Accepts an input file with a listing of symbols"""
#
def init():
    """Initializaton"""
    global gt, clstags, clstags1, clstags2, cur_price_clstags1, cur_price_clstags2, lnameside, rnameside, fldlst
    global fldcnt, linenum, rng, rng2, rng3
    gt = '>'; clstags = '</span></td>'; clstags2 = '</td></tr>'
    cur_price_clstags1 = '</span><div class'; cur_price_clstags2 = '</span><span class'
    lnameside = '<meta property="og:title" content="'; rnameside = ' ('
    fldlst = ["Price", "Name", "Previous Close", "Open", "Bid", "Ask", "Day&#x27;s Range", "52 Week Range", "Volume", "Avg. Volume"]
    fldlst += ["Market Cap", "PE Ratio (TTM)", "EPS (TTM)", "Forward Dividend &amp; Yield", "Ex-Dividend Date", "1y Target Est"]
    fldcnt, linenum, rng, rng2, rng3 = 0, 0, 200, 100, 10
#
def retrvsec(symbol):
    """Retrieves data for input symbol"""
    global gt, clstags, clstags1, clstags2, cur_price_clstags1, cur_price_clstags2, lnameside, rnameside, fldlst
    global fldcnt, linenum, rng, rng2, rng3
    try:
        info = dict()
        info['Symbol'] = symbol
        url = "https://finance.yahoo.com/quote/"+symbol+"?p="+symbol
        req = urllib.request.Request(url=url)
        response = urllib.request.urlopen(req)
        status_code = response.getcode()
        charset = response.info().get_content_charset()
        if charset == None:
            charset = 'utf-8'
        content = response.read().decode(charset).rstrip()
        for val in fldlst:
            if val == "Price":
                for ctags in (cur_price_clstags1, cur_price_clstags2):
                    srch = ctags
                    fnd = content.find(srch)
                    if fnd != -1:
                        fnd2 = content.find(gt, fnd - rng3)
                        info["Price"] = content[fnd2 + 1 : fnd]
                    else:
                        pass
            elif val == "Name":
                srch = lnameside
                fnd = content.find(srch)
                fnd2 = content[fnd : (fnd + rng2)].rfind(rnameside + symbol)
                info['Name'] = content[(fnd + len(lnameside)) : (fnd + fnd2)]
            else:
                srch = gt + val + clstags
                if srch in content:
                    fldcnt += 1
                    fnd = content.find(srch)
                    if val in ["Day&#x27;s Range","52 Week Range","Forward Dividend &amp; Yield"]:
                        fnd2 = content.find(clstags2, fnd + len(gt) + len(val) + len(clstags2), fnd + rng)
                        fnd3 = content.rfind(gt, fnd + len(gt) + len(val) + len(clstags2), fnd2)
                    else:
                        fnd2 = content.find(clstags, fnd + len(gt) + len(val) + len(clstags), fnd + rng)
                        fnd3 = content.rfind(gt, fnd + len(gt) + len(val) + len(clstags), fnd2)
                    info[val] = content[fnd3 + 1 : fnd2]
        return info
    except Exception as e:
        print(e)

def main():
    """Entry point of the program"""
    try:
        input_file = sys.argv[1]
        ifile_obj = open(input_file,'r')
    except IndexError:
        print("No input file provided - quitting.")
        return
    except FileNotFoundError:
        print("File",input_file,"not found - quitting.")
        return
    try:
        output_file = input("Enter the destination filename (use forward slash for path delimiter): ")   # i.e. "C:/data/stock-data.txt"
        ofile_obj = open(output_file,'w')
    except PermissionError:
        path = output_file.split('/')
        dir = ''
        for i in range(len(path) - 1):
            dir = dir + path[i] + '/'
        print("Verify your write privilege to the destination directory",dir)
        ifile_obj.close()
        return
    except FileNotFoundError:
        err = str(FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),output_file))
        print(err.split('[Errno 2] ')[1])
        ifile_obj.close()
        return
    init()
    for ticker in ifile_obj:
        symbol = ticker.rstrip()
        print(symbol)
        inf = retrvsec(symbol)
        if inf != None:
            ofile_obj.write(str(inf) + '\n')
            print(inf)
        else:
            print("Failed to retrieve security information for",symbol)
    ifile_obj.close()
    ofile_obj.close()
#
if __name__ == '__main__':
    main()
