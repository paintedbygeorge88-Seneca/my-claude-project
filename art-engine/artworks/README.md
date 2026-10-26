# Artworks go here

Two ways to add a painting. Both are fine.

**Quickest (from your phone or the GitHub website):** drop an image straight into this
folder, named after the painting, e.g. `salt-light.jpg`. That's it. The engine works out
the title from the filename and detects the colours itself.

**Better (more buyers find it):** make a folder per painting with the image and an
`info.yml` file. Or just tell Claude "add this painting" and send the photo. Claude
writes the file for you.

```
artworks/
  salt-light/
    artwork.jpg
    info.yml
```

`info.yml`. Every line is optional except `title`:

```yaml
title: "Salt Light No. 3"
year: 2025
medium: "Acrylic on canvas"
original_size: "100 x 80 cm"
description: "One or two sentences in your own voice about the piece."
colours: [ochre, deep blue, off-white]     # auto-detected if left out
mood: [calm, warm, coastal]
rooms: [living room, bedroom]              # where it would look good
keywords: [mediterranean art, large abstract canvas]
prices:
  - {size: "A3 print (30 x 42 cm)", price: 45}
  - {size: "A2 print (42 x 59 cm)", price: 75}
buy_links:
  - {label: "Buy print", url: "https://buy.stripe.com/..."}
  - {label: "On Etsy", url: "https://www.etsy.com/listing/..."}
original_available: true
sold: false
```

Photo tips: shoot square-on in daylight, crop to the canvas edge, and aim for at least
2000 px on the long side. The close-up "detail" pins zoom into your photo, so sharp
photos make much better pins.
