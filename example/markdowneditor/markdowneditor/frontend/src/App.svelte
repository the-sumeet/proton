<script>
  import "./app.css";
  import { get_files, set_dir, go_back, get_file_content } from "../proton/main/App";
  import { marked } from "marked";
  import Sidebar from "./Sidebar.svelte";

  let files = [];
  let file;
  let markdown = "";

  function getFiles() {
    get_files().then((data) => {
      files = data;
    });
  }

  $: if (file) {
    if (file.is_dir) {
      set_dir(file.path).then(() => {
        getFiles();
      });
    } else {
        get_file_content(file.path).then((data) => {
          markdown = data;
        });

    }
  }

  getFiles();

  function onGoBack() {
    go_back().then(() => {
      getFiles();
    });
  }
</script>

<!--
  This example requires updating your template:

  ```
  <html class="h-full bg-white">
  <body class="h-full">
  ```
-->
<div class="flex w-full h-screen">
  
  <!-- Sidebar -->
  <Sidebar onGoBack={onGoBack}  bind:file={file} {files} />

  <main class="flex flex-col h-screen w-4/5">
    <!-- Title -->
    <div class="flex">
      <span class="truncate p-2 font-bold border-b w-full"
        >
        {#if file}
        {file.name}
        {/if}
        </span
      >
      <span class="isolate inline-flex">
        <button
          type="button"
          class="relative inline-flex items-center bg-white px-3 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-10"
          ><i class="bi bi-floppy"></i></button
        >
        <button
          type="button"
          class="relative -ml-px inline-flex items-center bg-white px-3 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-10"
          ><i class="bi bi-copy"></i></button
        >
        <button
          type="button"
          class="relative -ml-px inline-flex items-center bg-white px-3 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-10"
          ><i class="bi bi-trash"></i></button
        >
      </span>
    </div>

    <div class="flex flex-1">
      <!-- Input -->
      <div class="flex-1 h-full">
        <textarea
          bind:value={markdown}
          class="border-r h-full block w-full bg-white px-3 py-1.5 text-base text-gray-900 placeholder:text-gray-400 sm:text-sm/6"
        ></textarea>
      </div>

      <!-- Preview -->
      <div class="flex-1 h-full">
        <div class="preview">{@html marked(markdown)}</div>
      </div>
    </div>
  </main>
</div>
