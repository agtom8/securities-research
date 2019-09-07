# 08/03/2019 ATOM
import sys
import ast
import pyodbc
"""Reads an input text file with stock information (as dictionary) and uploads the parsed data to an SQL Server database"""
#
def main():
    """Entry point of the program"""
    try:
        input_file = sys.argv[1]
        ifile_obj = open(input_file, 'r', encoding='utf-8')
    except IndexError:
        print("No input file provided - quitting.")
        return
    except FileNotFoundError:
        print("File",input_file,"not found - quitting.")
        return
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=localhost\\SQLEXPRESS;'
                          'Database=Securities;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    reccnt = 0
    input_dict = dict()
    for rec in ifile_obj:
        reccnt += 1
        input_dict = ast.literal_eval(rec.rstrip())
        symbol = price = prev = open_price = daymin = daymax = ftwmin = ftwmax = volume = avgvol = bid = bidqty = ask = askqty = mktcap = pe_ratio = eps = fdy = edd = oyte = None
        dontsave = 0
        for key, val in input_dict.items():
            if key == 'Symbol':
                symbol = val
                if len(symbol) < 1:
                    dontsave = 1
                    break
            elif key == 'Price':
                price = val.strip().replace(',','')
                if price.replace('.','').isdigit():
                    price = float(price)
                else:
                    dontsave = 1
                    break
            elif key == 'Name':
                name = val
                if len(name) < 1:
                    dontsave = 1
                    break
            elif key == 'Previous Close':
                prev = val.strip().replace(',','')
                if prev.replace('.','').isdigit():
                    prev = float(prev)
                else:
                    prev = None
            elif key == 'Open':
                open_price = val.strip().replace(',','')
                if open_price.replace('.','').isdigit():
                    open_price = float(open_price)
                else:
                    open_price = None
            elif key == 'Bid':
                if ' x ' not in val:
                    bid = bidqty = None
                    continue
                bid = val.split(' x ')[0].strip().replace(',','')
                if bid.replace('.','').isdigit():
                    bid = float(bid)
                else:
                    bid = None
                bidqty = val.split(' x ')[1].strip().replace(',','')
                if bidqty.replace('.','').isdigit():
                    bidqty = int(bidqty)
                else:
                    bidqty = None
            elif key == 'Ask':
                if ' x ' not in val:
                    ask = askqty = None
                    continue
                ask = val.split(' x ')[0].strip().replace(',','')
                if ask.replace('.','').isdigit():
                    ask = float(ask)
                else:
                    ask = None
                askqty = val.split(' x ')[1].strip().replace(',','')
                if askqty.replace('.','').isdigit():
                    askqty = int(askqty)
                else:
                    askqty = None
            elif key == 'Day&#x27;s Range':
                if ' - ' not in val:
                    daymin = daymax = None
                    continue
                daymin = val.split(' - ')[0].strip().replace(',','')
                if daymin.replace('.','').isdigit():
                    daymin = float(daymin)
                else:
                    daymin = None
                daymax = val.split(' - ')[1].strip().replace(',','')
                if daymax.replace('.','').isdigit():
                    daymax = float(daymax)
                else:
                    daymax = None
            elif key == '52 Week Range':
                if ' - ' not in val:
                    ftwmin = ftwmax = None
                    continue
                ftwmin = val.split(' - ')[0].strip().replace(',','')
                if ftwmin.replace('.','').isdigit():
                    ftwmin = float(ftwmin)
                else:
                    ftwmin = None
                ftwmax = val.split(' - ')[1].strip().replace(',','')
                if ftwmax.replace('.','').isdigit():
                    ftwmax = float(ftwmax)
                else:
                    ftwmax = None
            elif key == 'Volume':
                volume = val.strip().replace(',','')
                if volume.replace('.','').isdigit():
                    volume = int(volume)
                else:
                    volume = None
            elif key == 'Avg. Volume':
                avgvol = val.strip().replace(',','')
                if avgvol.replace('.','').isdigit():
                    avgvol = int(avgvol)
                else:
                    avgvol = None
            elif key == 'Market Cap':
                mktcap = val.strip()
            elif key == 'PE Ratio (TTM)':
                pe_ratio = val.strip()
            elif key == 'EPS (TTM)':
                eps = val.strip()
            elif key == 'Forward Dividend &amp; Yield':
                fdy = val.strip()
            elif key == 'Ex-Dividend Date':
                edd = val.strip()
            elif key == '1y Target Est':
                oyte = val.strip().replace(',','')
            else:
                pass
        if dontsave == 1:
            continue            # key fields must be present
        try:
            cursor.execute("""
                INSERT INTO Securities.Finyahoo.Secprice
                     (symbol, cur_price, prev_close, day_open, bid, bid_qty, ask, ask_qty, day_min, day_max, ftw_min, ftw_max, day_vol, avg_vol, mkt_cap, pe_ratio, eps, fwd_div_yld, exdiv_date, one_year_tgt_est)
                     VALUES   (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (symbol, price, prev, open_price, bid, bidqty, ask, askqty, daymin, daymax, ftwmin, ftwmax, volume, avgvol, mktcap, pe_ratio, eps, fdy, edd, oyte))
            conn.commit()
        except Exception as ex:
            print(ex)
    cursor.close()
    conn.close()
    ifile_obj.close()
    print("Processed",reccnt,"input records")

if __name__ == '__main__':
    main()
