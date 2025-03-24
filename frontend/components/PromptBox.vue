<script setup lang="ts">

const props = defineProps(['title', 'color', 'content'])


</script>

<template>
  <div
    :class="[
      'border rounded-lg px-4 flex flex-col',
      color === 'teal' && 'border-teal-300 bg-teal-300/20 text-teal-600',
      color === 'orange' && 'border-orange-300 bg-orange-300/20 text-orange-600',
      color === 'cyan' && 'border-cyan-300 bg-cyan-300/20 text-cyan-600'
    ]"
  >
    <p class="my-4 font-bold">{{title ?? "Result"}}</p>
    <p class="text-black mb-4">
        {{content}}
    </p>
  </div>
</template>
