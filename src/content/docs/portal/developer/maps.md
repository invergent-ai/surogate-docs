---
title: Maps
description: A location field, maps.yaml with its base maps and layers, the Map widget, the automatic map of a field, the action that saves a map, and the calls behind them.
---

The configuration behind [Maps](/portal/sites/maps/). That page covers what people see and the console's Maps page.

## A location field

In a model's file (`models/<id>.yaml`), a field of the type `location`:

```yaml
fields:
  locatie:
    type: location
    shape: point
    label: { ro: Sediu, en: Headquarters }
    required: true
```

- `shape`: `point`, `polygon` or `any` (when left out). Only a `location` takes it.
- It is a `jsonb` column. It is never `filterable` or `sortable`.
- Its value is GeoJSON in WGS84, **longitude first**: `{"type":"Point","coordinates":[23.5899,46.7712]}`, or a `Polygon` of one ring. The portal rounds coordinates to 7 decimals and closes a ring that is open. It refuses, naming the field and in Romanian, a longitude outside −180 to 180, a latitude outside −90 to 90, a ring with fewer than 3 different points or more than 1,000, a ring that crosses or touches itself, a polygon with holes, and any other shape.
- A field whose shape would go from `point` to `polygon` while points are kept is refused (`shape_change`); `any` always fits.
- CEL reads it as a map: `record.locatie.type`, `record.locatie.coordinates`. GraphQL has the scalar `GeoJSON`. A listing shows `46.771200, 23.589900` (latitude first) or `Polygon, 6 vertices`. CSV and XLSX exports give well-known text, `POINT(23.5899 46.7712)`.

In a form, the extension field `location`, in the **Extensions** group of the builder:

```yaml
- { type: location, key: locatie, label: Sediu, shape: point, input: true, validate: { required: true } }
```

`shape` is the same. A model's own form (`model-<id>`) uses it for every location field.

## maps.yaml

The base maps and the layers are one file at the top of the configuration, `maps.yaml` (the console's **Maps**):

```yaml
baseMaps:
  topo:
    name: { ro: Topografică, en: Topographic }
    type: xyz
    url: https://tile.opentopomap.org/{z}/{x}/{y}.png
    attribution: "Map data © OpenStreetMap contributors, SRTM | Map style © OpenTopoMap (CC-BY-SA)"
    minZoom: 0
    maxZoom: 17
    default: true
  ortofoto:
    name: { ro: Ortofotoplan, en: Orthophoto }
    type: wms
    url: https://wms.example.ro/ows
    layer: ortofoto2024
    version: "1.3.0"
    connector: ancpi
    attribution: © ANCPI
layers:
  lpis:
    name: { ro: Parcele LPIS, en: LPIS parcels }
    type: wfs
    connector: apia
    path: /geoserver/ows
    layer: "lpis:parcele"
    crs: 3844
    attributes:
      - { key: cod, label: { ro: Cod parcelă, en: Parcel code } }
    style: { color: "#b45309", fillColor: "#fbbf24", opacity: 0.35 }
    minZoom: 12
    attribution: © APIA
    view: [group:inspectors]
```

- **Ids** are `^[a-z][a-z0-9_]{0,19}$`. At most 20 base maps and 50 layers.
- **A base map:**
  - `type` is `xyz` (`url` holds `{z}`, `{x}`, `{y}`), `wmts` (`url`, `layer`, `format`, `tileMatrixSet` of web Mercator, `GoogleMapsCompatible` when left out, `style`) or `wms` (`url`, `layer`, `format`, `version`: `1.3.0` when left out, or `1.1.1`).
  - `attribution` is required, at most 300 characters. `minZoom` and `maxZoom` are whole numbers from 0 to 22.
  - At most one is `default: true`. **OpenStreetMap is built in as `osm`** and is the default until a base map with another `default: true`, or a base map called `osm`, is written.
- **A layer:**
  - `type` is `wms`, `wfs`, `ogc` (OGC API Features) or `geojson`. `layer` is the WMS layer, the WFS type name or the OGC collection; a GeoJSON address has none.
  - `connector` is required for `wfs`, `ogc` and `geojson`, optional for `wms` (which can have `url` instead). `path` goes with a connector. `version` is a WMS's or WFS's (`2.0.0` for a WFS when left out).
  - `crs` is `4326`, `3857` or `3844` (Stereo 70). For a WFS and an OGC API the view is asked in that system (`bbox=…,EPSG:3844`; OGC API: `bbox-crs` and `crs`), and every position of the answer is turned to WGS84. A WFS and a GeoJSON address take x as east and y as north. A GeoJSON address is read whole, kept a minute, and cut to the view.
  - `attributes`: up to 8, `{ key, label }`. Only these reach the page, as text. `style`: `color`, `fillColor` as `#rrggbb`, `opacity` from 0 to 1.
  - `minZoom`: 12 for objects, 0 for a WMS, when left out.
  - `view`: a list of [principals](/portal/developer/permissions/), checked as a model's `view` is. Left out, people signed in.
- **A connector** is a web connector (`kind: http`) that signs in as itself, not a per-person one. A base map's address must be on the connector's own address: its credentials are sent nowhere else. The portal asks a service over https, and over http only where the install lets it reach private networks.
- `portal check` refuses a connector, a base map or a layer that does not exist, wherever it is named.

## The calls

All under `/_portal/api/maps` at the host's tenant; a token needs the `data` scope.

| Call | Answers |
|---|---|
| `GET /config?locale=` | The base maps (`id`, `name`, `tiles`, `attribution`, `minZoom`, `maxZoom`, `default`) and the layers the caller may see. Never a service's address. |
| `GET /tiles/<base map>/<z>/<x>/<y>` | The tile, a PNG, JPEG, WebP or GIF as its first bytes say. 502 `map_unavailable` when the service fails, answers more than 2 MB, or sends no image. Kept an hour; 1,500 tiles a minute for one address. |
| `GET /features?model=&field=&record=&fields=&filter.<f>=&q=&locale=` | A GeoJSON `FeatureCollection` of the places the caller may see, each with `properties.__title` and `__rows`. 413 `too_many` past 5,000. |
| `GET /layers/<id>/features?bbox=w,s,e,n&zoom=&locale=` | The layer's objects in the view, in WGS84, with `truncated` past 5,000. 400 `zoom_too_far`, 403 for a layer the caller may not see, 502 `layer_unavailable`. |
| `GET /layers/<id>/tiles/<z>/<x>/<y>` | A WMS layer's tile, in web Mercator. |
| `GET /layers/<id>/info?lat=&lng=&zoom=` | What a WMS says is at a place: `{ rows }`. |
| `GET /snapshots?model=&record=&field=` | A record's saved maps, newest first (up to 10): `state`, `trigger`, `createdAt`, `missingLayers`, and `url` for those who may open the folder. |
| `POST /snapshots` `{ model, record, field }` | Asks for another map: 202 `{ id }`. A session only, never while seeing the portal as someone else. A map already waiting is the one asked for. |

## The Map widget

In a page's file:

```yaml
regions:
  main:
    - id: harta
      app: portal
      widget: map
      preferences:
        model: unitati
        field: locatie
        show: records        # record (when left out) or records
        baseMaps: [osm, topo]
        baseMap: topo
        layers: [lpis]
        layersOn: [lpis]
        height: 460
        fields: [cod, judet]
```

- `model` and `field` (a location field) are required. `show: record` takes the record from `?record=<id>` or any `?p_<placement>_record=<id>`.
- `baseMaps` and `layers` list what it offers (none: every base map, no layer); `baseMap` and `layersOn` are on at first and must be among them.
- `height`: 200 to 1,200. `fields`: at most 8, none a link.
- A listing takes `map: true`: the map of the model's first location field above its table.

## A field's automatic map

On a location field:

```yaml
fields:
  locatie:
    type: location
    snapshot:
      when: [change, state]
      stateField: stare
      states: [Transmisă]
      format: png
      size: { width: 1600, height: 1000 }
      baseMap: osm
      layers: [lpis]
      folder: dosare
```

- `when`: `change` (each save that changes the place), `state` (a save after which `stateField` holds one of `states`, from another value), or both.
- `format`: `png` (with an optional `size`, 800×600 to 3000×2000, 1200×800 when left out) or `pdf` (an A4 page, landscape).
- `folder` must exist and must not be public: `portal check` refuses a public one. `baseMap` and `layers` must exist.
- The save asks for the map in its own transaction, through the change queue that also feeds [jobs](/portal/developer/jobs/): a row of `map_snapshots`, with the place as it was saved. A worker on the server makes it after the save, as the person who saved, with three tries 15 seconds apart. A save is never held up, and a failure leaves the record as it was.
- The file is `<model>-<record id>-harta-<yyyymmdd-hhmmss>.<ext>` (the portal's time zone), a new one each time. It is at most 10 MB. A layer that does not answer is left out, and named on the picture and in the row's `missing_layers`.
- Text is drawn as outlines, so the machine needs no font.

## The action

`mapSnapshot`, in the Documents section:

```yaml
- type: mapSnapshot
  model: unitati
  record: vars.unit.id
  baseMap: osm
  layers: lpis
  format: pdf
  toFolder: dosare
  toName: '"harta-" + vars.unit.cod + ".pdf"'
  into: harta
```

- `record` (an expression giving an id, with `model`) or `geometry` (an expression giving GeoJSON), never both. With `record`, the run's person must see the record; its place is the model's first location field.
- `title` (an expression), `baseMap`, `layers` (ids, separated by commas), `format` (`png` when left out), `size` (`1600x1000`, PNG only), `toName` (named by the model and time when left out), `toFolder` and `into`.
- `into` gets `{ folder, name, missingLayers }`. The folder is asked before any work, as for other document actions. It cannot be used from a GET or public endpoint.
