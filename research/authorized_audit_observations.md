# Authorized read-only audit — app.sellerboard.com (observed 2026-09-10, IST)

Session: user's own logged-in Chrome session (Claude in Chrome), user login (redacted). Accounts available on switcher: 3 (Rama Amazon.in / INR; PWF Amazon.co.uk / GBP; a third not opened). No settings changed, no forms submitted, no exports downloaded. Only navigation, dropdown opens, modal opens (all cancelled). Screenshots taken for reference only, NOT included in deliverables (contain real revenue, SKUs, order IDs).

## Observed navigation (Amazon account context)
Top bar: view tabs per page; Help (?); History/clock icon; Light/Dark toggle; Alerts bell (badge); Account menu → {account list, Summary Dashboard (when >1 account), Add another account, Switch sellerboard account, Logged in as, Log out}.
Sidebar (non-accordion; Collapse control):
- Profit: Dashboard (/dashboard: Tiles | Chart | P&L (/dashboard/table) | Map (/dashboard/choropleth) | Trends), Products, Indirect Expenses (/expenses), Variable Expenses, LTV, Cashflow, Reports (/export)
- PPC: Dashboard (/ppc), Recommendations (/ppc/recommendations), Automation Log (/ppc/log)
- Inventory: Planner (/inventory), Purchase Orders, FBA Shipments, Suppliers
- Autoresponder: Campaigns, Products, Orders
- Money Back: Lost & Damaged, Returns, FBA Fee Changes
- Alerts: Dashboard (/alerts), Settings (/alerts/settings)
- Keyword Research (/keywordResearch)
- eBay: Dashboard, LTV, Products, Orders, Expenses (not connected in this account → "Connect eBay Account" CTA)
- QuickBooks: Settlements (beta), Configuration of QB accounts (not connected → connect CTA)
- Settings: General (/settings), MCP Connector (beta) (/settings/mcp), Automation (/settings/automation), Billing (/billing)
NOT present in these accounts' nav: Walmart, Repricer, Search Terms, Amazon Attribution, Reseller workflow. (Likely gated by connected marketplace/Brand Registry/rollout — Unknown; blog says Repricer live 3 Sep 2026.)
Summary Dashboard (multi-account): Tiles | Chart | P&L; filter "All accounts"; reduced sidebar (Dashboard, Settings General, MCP Connector).
Popup on login: "New feature — PPC Day Parting (beta)" — bids adjusted 4×/day by order activity (Observed, feature not audited further).

## Dashboard — Tiles
Tiles: Today, Yesterday, Month to date, This month (forecast), Last month (each: Sales w/ % vs prior, Orders/Units, Refunds, Adv. cost, Est. payout, Gross profit, Net profit w/ %; "More" opens popover).
Controls: Search (products; Select all/Unselect all), Period dropdown (presets: Today/Yesterday/MTD/Forecast/Last month; Today/Yesterday/MTD/Last month; Today/Yesterday/7d/14d/30d; This week/Last week/2 weeks ago/3 weeks ago; MTD/Last month/2 months ago/3 months ago; Today/2 days ago/3 days ago; Today/7 days ago/8 days ago; This quarter/Last quarter/2 quarters ago/3 quarters ago; Custom range; "Configure tiles"), All marketplaces dropdown, Filter button, Compare (Do not compare / Compare with previous period / Compare Year over Year).
"More" popover rows (expandable ▸): Sales, Units, Refunds, Promo, Advertising cost, Shipping costs, Giftwrap, Refund cost, Amazon fees, Cost of goods, VAT, Gross profit, Indirect expenses, Net profit, Estimated payout, TACOS, % Refunds, Sellable returns, Margin, ROI, Active subscriptions (SnS), Sessions, Unit session percentage.
Amazon fees expansion (Amazon.in observed fee names): FBA storage fee, FBA weight based fee, Fixed closing fee, FBA per unit fulfillment, Affordability expense, Item TDS, Payment retraction, Technology fee, FBA removal fee, Adjustment FBA per unit, Free replacement refund, Adjustment FBA weight, Reversal reimbursement, … (list continues; tooltip: "All amazon expenses … including account-level fees").
Lower table: tabs Products | Order Items; Group by (—, ASIN, Parent, Marketplace, Brand, Supplier, Channel, Coupon, …); download icon; column-picker icon. Product columns: Product (image, ASIN·SKU, title, price, COGS, FBA stock link), Units sold, Refunds, Sales, Ads, % Refunds, Sellable returns, Gross profit, Net profit, Margin, ROI, BSR (with trend arrow), Average selling price, TACOS, … Row links: ASIN→amazon.in/dp, COGS→edit, FBA stock→/inventory?p=<uuid>.
State persistence: last dashboard view (e.g., Map) is remembered on return (Observed).

## Dashboard — Chart
Period "Last 12 months, by month"; Configuration link; series Units sold / Advertising cost / Refunds / Net profit; bar+line combo; right-hand P&L summary panel (same rows as "More"); lower product table "All Periods".
## Dashboard — P&L (table)
Columns per period (month or day), rows = P&L lines (expandable); Heatmap on/off; Compare; period picker.
## Dashboard — Map
Sales/Stock radio; choropleth; "All regions" table: Region/Product, Stock, Orders, Units sold, Sales, Amazon fees, Sellable returns, Cost of goods, Refund cost, VAT, Gross profit, Info; period Last 12 months/3 months/30 days/Custom.
## Dashboard — Trends
Metric tabs: Sales, Orders, Advertising cost, TACOS, Refunds, Refund cost, Amazon fees, Net profit, Margin, ROI, Sessions, Other (Units, Promo, …); per-product sparkline; monthly columns incl. "September forecast"; cell % change vs prior; Heatmap on/off; export icon; Compare.

## Products
Filters: Search, Any COGS, condition (New / New + Grade and Resell), Filter; Group by. Columns: Product, Tags, COGS, Value of unsellable returns (%), Shipping profile ("Custom (₹0.00)"), Profit per unit, Sales velocity (units/day), VAT rate. Bottom actions: Import, Export, Show hidden, Hide, Create multi-product batch, Refresh, Save. Row checkbox bulk selection.
Edit COGS screen: tabs Batches; marketplace tabs (Amazon.in | Multi-channel); columns Receipt date, Accounting method (By period / Weighted average / FIFO), Units, Unit cost, Comment; "Edit cost elements" link (landed-cost elements); Add new batch; Close / Save.

## Indirect Expenses
Rows: date, frequency (Daily / One-Time / …), name, tag/SKU assignment (Search by name, tag, SKU), checkbox, marketplace (All marketplaces), currency, amount; monthly total; pagination; Add / Import / Export / Save.
## Variable Expenses
Columns: Creation date, Title, Calculate expense as, Amount, Category, Conditions, Start, End, Actions; filters All products / All categories / All marketplaces; Add.
## LTV
Tiles: Acc. sales per buyer (₹), Acc. sales per buyer (units), Acc. orders per buyer — each for Last 3/6/12/24 months; per-product table with 3/6/12/24-month windows; Period + marketplace filter; Apply.
## Cashflow
"Last 12 months by payout"; line chart cash on hand; Configuration; table Date, Description, Type (Payout), Sum, Cash on Hand, Delete; Import / Export / Add.
## Reports (/export)
Report list: Dashboard by day; Dashboard by month; Dashboard by product; Orders; Sales by product/month; Advertising Performance Report; Repeat customers (by brand); Stock history report; Cost of Goods Sold; Refunds. (Each opens a parameter/export flow — not executed.)

## PPC
Dashboard: Search, All campaigns, period "Last 30 days, by day", All campaign statuses, More filters, Filter; Configuration; chart Ad spend / Profit / ACOS; summary panel: PPC sales, Orders, Promo, Ad spend, Refunds, Amazon fees, COGS, VAT, Expenses, Profit (estimated), Average CPC, ACOS. Tabs: Portfolios | Campaigns | Ad groups | Keywords | Search terms. Columns: Name (type badge SP, marketplace flag), Status (dropdown), Ad spend, ACOS, Profit, Break-even ACOS, Daily budget, Budget utilization, Current bid, Bid recommendation, Bid recommendation strategy…; actions Edit, Accept recommendations, export, column picker; "Create smart portfolio"; Save.
Recommendations: tabs Bids | Well performing search terms | Poorly performing search terms | Budget adjustments | Keyword isolation; columns Campaign/Ad group, Keyword, Current bid, Bid recommendation (info), PPC sales, Ad spend, ACOS, Actions (accept ✓, snooze 🔔); bulk Accept / Snooze for 30 days.
Automation Log: tabs Completed | Pending; columns Date, Campaign, Ad group, Keyword, Change type, Bid recommendation strategy, Comment; period filter; All changes; Export.

## Inventory
Planner: tiles Action required (Restock & reorder: Products, Funds needed, Est. monthly sales at risk, Est. monthly profit at risk), Total, FBA, Prep. stock, Ordered (Units, Cost of goods, Potential sales, Potential profit); filters condition, FBA, marketplaces, Show OOS items, Filter. Table: Product, FBA/FBM stock, Reserved, Sales velocity (units/day), Days of stock left (badge), Sent to FBA, Prep center stock, Ordered, Days until next order (badge, negative = overdue), Recommended quantity for reordering, Stock value, ROI…; Import / Export / Create purchase order.
Purchase Orders: status tiles Draft / Ordered / Shipped (PO count, Total cost, Total units); table PO date, PO number, Supplier, Products, Total units, Total cost, Estimated arrival, Comment, FBA shipments, Status, Actions; Create purchase order.
FBA Shipments: period, All statuses; table Shipment plan/ID, Date, Destination (FC code), % units received, Products, Status (In transit / Working …), Last update, Purchase orders, Comment, Actions; Export / Refresh.
Suppliers: Supplier name, Currency, Email, Website, Comment, Actions; Add.

## Autoresponder
Campaigns: Priority, Name, Products, Status, Last status change, Sent today, Sent last 30 days, Actions; New campaign. Orders: Order date, Shipping date, Delivery date (estimated), Order number, Marketplace, Products, Campaign, Status (Pending Data…), Last sent date, Black listed (Yes/No), Actions; filters Order ID, All campaigns.

## Money Back
Lost & Damaged: "Estimated reimbursement amount" + last update date; 3-step guidance (How it works / Download report (Excel/CSV; period imported into sellerboard, max 60 days) / Contact seller support with category instructions). Returns: same pattern (max 105 days; start date picker; warning to verify before filing). FBA Fee Changes: period picker (e.g., last 18 months), Excel/CSV, seller-support category guidance. No in-app case submission (Observed: manual via Seller Support).

## Alerts
Dashboard: tiles Major / Minor / Total (Unresolved, Resolved); tabs All | By product | By type | By priority | By marketplace; table Date, Description (e.g., image changed, shipment deviation, running out of stock, time to reorder), Product, Comment, Marketplace, Priority, Resolved checkbox; Mark all as resolved; Export.
Settings: tabs Configure alert types | Exclude products/marketplaces; categories Product alerts, Financial alerts, Performance alerts, Inventory alerts, Amazon advertising recommendations; per category Priority, Notification in sellerboard / in Seller Central / per E-mail, Recipients list (override default).

## Keyword Research
Search by keywords or ASINs; marketplace selector (Amazon.in); Brand Analytics based.

## Settings
General: Accounts card (name, marketplace, currency) with connector chips: Selling Partner API (SP-API) ✓, Advertising API (PPC) ✓, Facebook, Snapchat, Pinterest, TikTok, Google Ads, Veeqo, Walmart (modal: select US/MX/CA → OAuth redirect), Walmart Ads (disabled until Walmart), ShipStation, QuickBooks; Add account. "sellerboard for Shopify connector" section (Connected / Disconnect rows; How to connect) — confirms an Amazon→Shopify connector exists in .com (Observed, not exercised). Other settings note: user settings (password, language, 2FA) live on account-selection page.
Account Settings modal tabs: GST (India): "Amazon fees include GST and I'll be able to recover it" + start date; "Treat TCS as Recoverable"; "Add local GST to the advertising costs". FBM Pick & Pack: price per package, price per item, different price for first X items. Calculation Logic: Ignore multi-channel orders; Ignore deferred refunds until released; Don't show FBA shipping chargeback and giftwrap; Ignore FBA inbound shipment costs (select from: FBA inbound convenience fee, inbound defect fee, carton level info fee, Inbound transportation, Inbound transportation program fee, FBA international inbound freight fee, …freight tax and duty, Global inbound transportation duty/freight); Amortize Amazon fees daily (0 of 19 fees); Assume pending returns are unsellable; Consider returned item's condition despite Restocking fee; COGS for oversold units (FIFO): Last batch / Zero / Fixed; FBM shipping cost for multi-product orders: Sum / Highest; Use net sales for margin calculation; Automatically reduce prep center stock when FBA inbound shipped (default prep center 1–4; start date). Data Retention: keep >18 months (retention period N months, e.g., 60) vs auto-delete after 18 months. Other Settings: Autoresponder sender email; Cashflow account start date; daily sales report email + time; Ignore inactive listings; Enable dashboard currency switch; Show reorder alerts on Planner page.
MCP Connector: closed beta; read-only access for AI assistants to dashboard metrics, products, COGS; waitlist.
Automation: table Automation type, Periodicity, Format, Retrieve method, Email/Link, Actions; Renew links; Add.
Billing: payment method (card on file — details not recorded), current plan (observed: Business, USD 39/month, billed monthly), Manage subscription, Change billing cycle, billing info, invoices (date, number, amount, preview, download).
User settings (account-selection page): login e-mail, 2FA policy (Sometimes e.g. for new devices / …) with Authenticator app (enable) and Email (enabled), password, language, Demo mode checkbox, newsletter.
Not observed: user invitation / access-rights screen (plan-gated per public pricing: Enterprise) — Unknown.
