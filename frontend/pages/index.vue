




<script setup>
import { ref } from "vue";

const selectedImage = ref(null);
const imageFile = ref(null);
const replicateText = ref("");
const addText = ref("");
const isLoading = ref(false);

const generatedPrompt = ref("");


const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    imageFile.value = file;
    selectedImage.value = URL.createObjectURL(file);
  }
};

const submitData = async () => {

  isLoading.value = true;

  if (!imageFile.value || !replicateText.value || !addText.value) {
    alert("Please complete all fields!");
    return;
  }

  const formData = new FormData();
  formData.append("image", imageFile.value);
  formData.append("replicate", replicateText.value);
  formData.append("add", addText.value);

  try {
    const response = await fetch("http://127.0.0.1:8012/generate", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    console.log("Server Response:", data);
    generatedPrompt.value = data.prompt
  } catch (error) {
    console.error("Error submitting data:", error);
  }


  isLoading.value = false;



};
</script>



<template>

    <div class="w-full  flex flex-col justify-center items-center pt-[60px] pb-64">
        
        <h1 class="text-black text-3xl my-8 font-standard">
            Generate Image 
        </h1>


        <!-- IMAGE UPLOAD -->
        <div class="w-2/3 flex flex-col justify-start my-8">
          <p class="text-black my-4">1. Upload reference image</p>
          <div class="flex flex-row justify-start items-end w-full">
            <label class="h-64 border border-black rounded-lg flex justify-center items-center cursor-pointer hover:bg-neutral-300" style="aspect-ratio: 1;">
              <input type="file" @change="handleImageUpload" accept="image/*" class="hidden" />
              <img v-if="selectedImage" :src="selectedImage" class="h-full rounded-lg object-cover" />
              <span v-else class="text-black text-2xl">+</span>
            </label>
          </div>
        </div>


        <!-- WHAT TO REPLICATE -->
        <div class="w-2/3 my-8">
          <p class="text-black my-4">2. What you want to replicate?</p>
          <textarea
            v-model="replicateText"
            placeholder="Write description"
            class="w-full h-32 border border-black rounded-lg text-black p-4"
          ></textarea>
        </div>


        <!-- WHAT TO ADD -->
        <div class="w-2/3 my-8">
          <p class="text-black my-4">3. What you want to add?</p>
          <textarea
            v-model="addText"
            placeholder="Write description"
            class="w-full h-32 border border-black rounded-lg text-black p-4"
          ></textarea>
        </div>


        <Button title="Generate" :icon="'i-heroicons-arrow-right-20-solid'" :style="'white'" class="my-12" @click="submitData" :loading="isLoading"/>


        <div class="w-2/3 my-8">
          <p class="text-black my-4 text-center">{{generatedPrompt}}</p>
        </div>

    </div>

</template>