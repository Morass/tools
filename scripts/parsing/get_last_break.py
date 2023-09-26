import sys
from pathlib import Path

CLIENT = sys.argv[1]
INSTRUMENT = sys.argv[2]
YDRIVE = Path(r"Y:")
TRADING_MANAGER = YDRIVE/"Jhb"/"FAReports"/"AtlasEndOfDay"/"TradingManager"


def main():
    print(f"Looking for {CLIENT} and {INSTRUMENT}...")
    date_directories = sorted(list(TRADING_MANAGER.glob("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]")), reverse=True)
    for d in date_directories:
        try:
            cash_recon = list(d.glob('PS_CashReconTool_YTD*'))[0]
        except Exception:
            # List out of bounds + Nonexistence
            continue
        client = "XXX"
        visited = set()
        for line in cash_recon.read_text().split("<Row>"):
            # Line defining client:
            if line.startswith('<Cell ss:StyleID="client_title"><Data ss:Type="String">'):
                client = line.replace('<Cell ss:StyleID="client_title"><Data ss:Type="String">', "").split("<")[0]
                # Stop iteration after first revisited client
                if client in visited:
                    print(f"{d.name}: NOT FOUND")
                    # TODO: Check if return or break
                    break
                visited.add(client)
            else:
                # Do not care here -- not our client
                if client != CLIENT:
                    continue
                # Not a line with instrument
                if not line.startswith('<Cell ss:StyleID="value_general"><Data ss:Type="String">'):
                    continue
                # Not our instrumnet
                if INSTRUMENT not in line:
                    continue
                if "Break" in line:
                    print(f"{d.name}: BREAK")
                    break
                print(f"{d.name}: OK")
                return

main()
