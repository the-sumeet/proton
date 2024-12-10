<script>
    export let onGoBack;
    export let file;
    export let files = [];

    $: sortedFiles = files.sort((a, b) => {
        if (a.is_dir && !b.is_dir) return -1;
        if (!a.is_dir && b.is_dir) return 1;
        return a.name.localeCompare(b.name);
    });

    $: console.log(file);

    function select(f) {
        file=f;
    }

    function isMarkdown(f) {
        if (f.is_dir) {
            return true;
        }
        return f && f.name.endsWith(".md");
    }
</script>
<div class="w-1/5 border-r h-full">
    
    <div
      class="flex flex-col grow gap-y-5 border-gray-200 bg-white h-full"
    >
      <!-- Explorer buttons  -->
      <div class="flex shrink-0 items-center w-full h-min">
        <span class="isolate inline-flex w-full">
          <button
          on:click={onGoBack}
            type="button"
            class="py-2 flex-1 relative inline-flex items-center justify-center rounded-l-md bg-white px-3 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-10"
            ><i class="bi bi-arrow-left"></i></button
          >
          <button
            type="button"
            class="flex-1 relative -ml-px inline-flex items-center justify-center bg-white px-3 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-10"
            ><i class="bi bi-file-earmark-plus"></i></button
          >
          <button
            type="button"
            class="flex-1 relative -ml-px inline-flex items-center justify-center  bg-white px-3 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-10"
            ><i class="bi bi-arrow-clockwise"></i></button
          >
        </span>
      </div>

      <!-- Files list -->
      <nav class="overflow-y-auto flex flex-1 flex-col h-full">
        <ul role="list" class="flex flex-1 flex-col gap-y-1">
          {#each sortedFiles as file}
            <li>
              <a
                on:click={() => select(file)}
                href="#"
                class="{isMarkdown(file) ? "" : "cursor-not-allowed"} group flex gap-x-3 rounded-md p-2 text-sm/6 font-semibold text-gray-700 hover:bg-gray-50 hover:text-indigo-600"
              >
                {#if file.is_dir}
                <i class="bi bi-folder2"></i>
                {:else}
                <i class="bi bi-file-earmark"></i>
                {/if}
                {file.name}
              </a>
            </li>
          {/each}
        </ul>
      </nav>
    </div>
  </div>