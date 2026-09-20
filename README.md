# Ramla — Multi Unit Offer

Production: https://ramla-multi-unit-offer.vercel.app/

Two separate unit experiences under one comparison page:
- `/r1-78`: Dunes C3, 245 sqm BUA / 660 sqm plot / 57 sqm terrace, 22 original pages.
- `/r5-46`: Acacia C6, 246 sqm BUA / 681 sqm plot / 59 sqm terrace, 34 original pages.

Both offers retain the original PDFs, interactive room plans, scroll-driven map journeys, finishing details, installment schedules, downloadable self-contained HTML and WhatsApp Open Graph metadata.

The comparison page includes side-by-side floor plans with interactive room modals and a complete masterplan with red unit outlines. Compact annotations show each villa's type, price, land area, BUA and bedroom count. Tap a villa to zoom; double-tap the map or select “Show both villas” to reset.

R5-46 has 93 installment rows across three schedules. Unit and maintenance totals were checked against the PDF. Its bullet-plan dates are reproduced unchanged and prominently flagged: the source labels an eight-year plan but dates extend to 2044.

Local server: `python3 -m http.server 4176 --bind 127.0.0.1 --directory dist`
Deploy: `vercel deploy --prod --yes --scope youssefs-projects-94b1f3d5`

The build scripts record construction from the source files; they are not intended to be rerun on an already transformed dist folder without restoring the original single-offer source copy.

The `dist` directory is the current deployable website. Root-level component files and Python scripts preserve the source used to assemble it. Local annotation design experiments are available at `/annotation-options.html` and excluded from Vercel deployments.
