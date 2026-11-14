---
title: File management actions
description: The settings of the actions that copy, move and rename files, read their details, resize images, make and unpack ZIP archives, and exchange files with a server.
---

The configuration behind [File management actions](/portal/sites/file-management/). That page says what each action does for people, who may use it and its limits.

These go in an action list: a form's `actions` (`forms/<id>.yaml`), a flow, an endpoint or a job.

## Copy, move and rename a file

| Type | What it does | Takes |
|---|---|---|
| `copyFile` | Writes a copy of a file, in the same folder or another | `folder`, `name`, `toFolder`, `toName`, `replace` |
| `moveFile` | Writes the copy, then removes the file it came from | `folder`, `name`, `toFolder`, `toName`, `replace` |
| `renameFile` | Gives a file another name in its folder | `folder`, `name`, `toName`, `replace` |

- `name` and `toName` are expressions; `folder` and `toFolder` name folders.
- A file keeps its extension: a PDF copied as `report.txt` fails with "A file keeps its extension: .pdf.".
- A file already there under `toName` makes the action fail with "A file of that name is already there.", unless `replace: true`. Only someone who edits the folder may replace a file.
- Copying a file onto itself, or renaming it to the name it has, fails with "The file already has this name.".
- When a move has written the copy but cannot remove the file it came from, it fails and says so. Both files are then there; remove the old one by hand.

## A file moved where it belongs

```yaml
- type: moveFile
  folder: inbox
  name: '"cerere-" + submission.id + ".pdf"'
  toFolder: approved
  toName: '"cerere-" + submission.id + ".pdf"'
```

- `folder` and `name`: the file to move.
- `toFolder` and `toName`: where it goes, and its name there.

A file renamed in its folder, replacing one of that name:

```yaml
- type: renameFile
  folder: reports
  name: '"draft.pdf"'
  toName: '"final.pdf"'
  replace: true
```

- `replace: true`: a file already named `final.pdf` is replaced.

## Read a file's details

`fileInfo` keeps a file's details in `vars.<into>` as `{ folder, name, size, type }`: its size in bytes and the type it is served as, such as `application/pdf`. When there is no such file it keeps `null`, so an action list can check whether a file is there before it makes one (see [The details of a file](#the-details-of-a-file)).

## The details of a file

```yaml
- type: fileInfo
  folder: reports
  name: '"raport-" + vars.month + ".pdf"'
  into: report
- type: copyFile
  condition: vars.report != null
  folder: reports
  name: vars.report.name
  toFolder: archive
  toName: vars.report.name
```

- `into`: where the details are kept, or `null` when there is no such file.
- The copy is made only when the report is there.

## Images

`resizeImage` makes a resized copy of an image, such as a small preview of a photo someone uploaded (see [A thumbnail of an uploaded photo](#a-thumbnail-of-an-uploaded-photo)):

- `width` and `height`: whole numbers from 1 to 4000, as expressions; at least one of them.
- `fit`: `inside` (when left out) keeps the proportions within the width and height; `cover` fills them, cropping the middle; `contain` fits the whole image and pads the rest, white for a JPEG, transparent otherwise.
- `toName`: its extension decides the format: `.jpg`, `.jpeg`, `.png`, `.webp` or `.avif`.
- A copy is never larger than the image itself, and it is turned the right way up. When the width and height make a box larger than the image, the box shrinks whole, keeping its shape.
- JPEG, PNG, WebP, AVIF and still GIF images are resized. An animated image, an image of more than 40 million pixels (16 million for AVIF), or any other file fails, saying why.

`imageInfo` keeps an image's `{ width, height, format }` in `vars.<into>`, turned the right way up, or `null` when the file is not such an image or is not there.

## A thumbnail of an uploaded photo

```yaml
- type: resizeImage
  folder: photos
  name: '"foto-" + submission.id + ".jpg"'
  toFolder: thumbnails
  toName: '"foto-" + submission.id + ".webp"'
  width: "320"
  height: "320"
  fit: cover
```

- `width` and `height`: the box, here a square of 320 pixels.
- `fit: cover`: the photo fills the square, its middle kept.
- `toName`: a `.webp` name makes a WebP image.

## Files on a server

These actions exchange files with an FTP, FTPS or SFTP server, through a [file server connector](/portal/sites/connectors/#file-servers):

| Type | What it does | Takes |
|---|---|---|
| `ftpUpload` | Sends 1 to 20 files of a folder to the server, each under its own name | `connector`, `folder`, `names` (a list), `remoteDir`, `replace` |
| `ftpDownload` | Fetches one file into a folder | `connector`, `remotePath`, `toFolder`, `toName`, `replace` |
| `ftpList` | Lists a directory of the server | `connector`, `remoteDir`, `into` |
| `ftpDelete` | Removes a file on the server | `connector`, `remotePath` |

- `remoteDir` and `remotePath` are expressions, under the connector's directory: names separated by `/`, never `.` or `..`. A path going above the directory fails before the server is reached.
- `ftpUpload` refuses a name the server already has, before sending anything, unless `replace: true`. A file is sent under a temporary name and renamed when whole, so whoever reads the server never sees half a file.
- `ftpList` keeps a list of `{ name, size, directory, modified }`, at most 1,000 entries; `modified` is a date when the server gives one plainly, else `null`.
- `ftpDownload` of an empty file fails: the portal keeps no empty file.
- `ftpDelete` of a file that is not there is no error.
- The server's own messages are never shown: a failure says what went wrong in the portal's words, such as "The server refused the username, password or key."

## Files sent to a server and fetched from it

```yaml
- type: ftpUpload
  connector: registry
  folder: approved
  names: '["cerere-" + submission.id + ".pdf"]'
  remoteDir: '"incoming"'
- type: ftpDownload
  connector: registry
  remotePath: '"answers/raspuns-" + submission.id + ".pdf"'
  toFolder: answers
  toName: '"raspuns-" + submission.id + ".pdf"'
```

- `connector`: a file server connector.
- `names`: the files of `folder` to send.
- `remoteDir`: where they go, under the connector's directory.
- `remotePath`: the file to fetch, and `toFolder` and `toName`: where it is kept.

## ZIP archives

| Type | What it does | Takes |
|---|---|---|
| `zipFiles` | Packs files into a `.zip` | `folder`, `names` (a list; every file of the folder when left out), `toFolder`, `toName`, `replace` |
| `zipNames` | Lists the files in an archive | `folder`, `name`, `into` |
| `unzipFile` | Writes each file of an archive into a folder | `folder`, `name`, `toFolder`, `into` (optional), `replace` |

- An archive holds 1 to 100 files. Its name ends in `.zip`.
- `zipNames` keeps a list of `{ name, size }`, each name as the archive holds it, with its folders.
- `unzipFile` keeps the names it wrote in `vars.<into>`, in the archive's order.
- Without `replace: true`, a file already there makes the whole archive fail.

## An archive packed and unpacked

```yaml
- type: zipFiles
  folder: reports
  toFolder: archive
  toName: '"rapoarte-" + vars.month + ".zip"'
```

- `names` is left out, so every file of `reports` is packed.
- `toFolder` and `toName`: where the archive is kept.

```yaml
- type: unzipFile
  folder: uploads
  name: '"documente.zip"'
  toFolder: received
  into: received
```

- `folder` and `name`: the archive.
- `toFolder`: where its files are written.
- `into`: the names written, in the archive's order.

## Who may do what

An action that changes files changes the portal, so a GET or public [endpoint](/portal/sites/endpoints/) cannot use it. `fileInfo`, `zipNames` and `imageInfo` only read, and can be used anywhere. The actions on a server all reach another computer, so none of them is in a GET or public endpoint, `ftpList` included.

## Limits

- A file sent or fetched is at most 10 MB; one `ftpUpload` sends 50 MB at most.
