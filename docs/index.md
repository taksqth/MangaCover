---
layout: page
title: MangaCover
---

## Can you judge a manga by its cover?

This is a personal project for the [Fast.ai MOOC](https://course.fast.ai). The objective
is to build an ML product that labels a manga from its cover image.

<form id="cover-form" method="post" enctype="multipart/form-data">
    <div>
        <label for="cover-upload">Choose images to upload (PNG, JPG)</label>
        <input type="file" id="cover-upload" name="file" accept="image/*">
    </div>
   <div class="preview">
        <p>No files currently selected for upload</p>
    </div>
    <div>
        <button>Submit</button>
    </div>
</form>
<div class="result"></div>
<script type="text/javascript" src="assets/js/main.js"></script>