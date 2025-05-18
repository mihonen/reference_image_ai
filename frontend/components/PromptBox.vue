<script setup lang="ts">
import { ref, watch, nextTick, onMounted } from 'vue'

const props = defineProps(['title', 'color', 'content'])
const emit = defineEmits(['update:content'])

const localContent = ref(props.content)
const isEditing = ref(false)
const editableDiv = ref<HTMLElement | null>(null)

watch(() => props.content, (newVal) => {
  if (!isEditing.value) localContent.value = newVal
})

function toggleEdit() {
  isEditing.value = !isEditing.value
  if (isEditing.value) {
    nextTick(() => {
      if (editableDiv.value) {
        editableDiv.value.textContent = localContent.value
        placeCursorAtEnd(editableDiv.value)
        editableDiv.value.focus()
      }
    })
  } else {
    if (editableDiv.value) {
      localContent.value = editableDiv.value.textContent || ''
    }
    emit('update:content', localContent.value)
  }
}

function onInput() {
  // avoid reactive update while editing — we'll sync on "done"
}

function placeCursorAtEnd(el: HTMLElement) {
  const range = document.createRange()
  const sel = window.getSelection()
  range.selectNodeContents(el)
  range.collapse(false)
  sel?.removeAllRanges()
  sel?.addRange(range)
}
</script>

<template>
  <div
    :class="[
      'border rounded-lg px-4 py-2 flex flex-col relative',
      color === 'teal' && 'border-teal-300 bg-teal-300/20 text-teal-600',
      color === 'orange' && 'border-orange-300 bg-orange-300/20 text-orange-600',
      color === 'cyan' && 'border-cyan-300 bg-cyan-300/20 text-cyan-600'
    ]"
  >
    <p class="my-2 font-bold">{{ title ?? "Result" }}</p>

    <div
      v-if="isEditing"
      ref="editableDiv"
      class="text-black mb-4 outline-none border border-dashed border-gray-400 p-2 rounded min-h-[3rem] bg-white whitespace-pre-wrap"
      contenteditable
      @input="onInput"
    ></div>

    <p v-else class="text-black mb-4 whitespace-pre-wrap">{{ localContent }}</p>

    <button
      class="self-end text-md cursor-pointer text-blue-600 underline"
      @click="toggleEdit"
    >
      {{ isEditing ? 'Done' : 'Edit' }}
    </button>
  </div>
</template>
