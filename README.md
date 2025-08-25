
# Flask Suite v2

Modular Flask project with six apps and sub-app landing pages.

## Apps & Sub-apps
1. **Personal**
   - Favorites
   - Contact List
2. **Reference**
   - Circuit Inventory
   - HW Inventory
3. **CUCM Report**
   - SIP Trunk
   - RIS Report
4. **CUCM Tool**
   - AA Enable/Disable
   - EM Login/Logout
5. **IOS Report**
   - VLAN Report
   - Interface Details
6. **IOS Tool**
   - MGCP/SCCP Bouncing
   - Interface Bouncing

## Quickstart
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask --app app.py run --debug
```
Open http://127.0.0.1:5000

## Notes
- Bootstrap 5 + Bootstrap Icons via CDN.
- Each sub-app is a simple placeholder route to extend later.
