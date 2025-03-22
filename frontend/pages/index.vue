




<script setup>
import { ref } from "vue";

const selectedImage = ref(null);
const imageFile = ref(null);
const replicateText = ref("");
const addText = ref("");
const isLoading = ref(false);
const generatedPrompt = ref("");

const references = ref([]);


const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    imageFile.value = file;
    selectedImage.value = URL.createObjectURL(file);
  }
};

const generatePrompt = async () => {

  isLoading.value = true;

  let refs = references.value;

  let featureset = ""

  for (let i = 0; i < refs.length; i++){

    let r = refs[i]

    if (r.resultPrompt){
      featureset += r.annotationDescription + "\n";
      featureset += `Information extracted from reference image ${i}: \n` 
      featureset += r.resultPrompt
    }
  }

  const formData = new FormData();
  formData.append("extracted_features", featureset);
  formData.append("prompt", replicateText.value);

  try {
    const response = await fetch("http://127.0.0.1:8012/generate_prompt", {
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


const updateImage = (id, file) => {
  // Find the reference by ID and update the image and file
  const reference = references.value.find(ref => ref.id === id);
  if (reference) {
    reference.imageFile = file; 
  }
};

const modifyReference = (id, updatedData) => {
  const index = references.value.findIndex(ref => ref.id === id);
  if (index !== -1) {
    references.value[index] = { ...references.value[index], ...updatedData };
  }
};

const addReference = () => {
  references.value.push({
    id: Date.now(), // Unique ID for each reference
    selectedImage: null,
    imageFile: null,
    annotation: "Style",
    annotationDescription: "",
    isLoading: false,
    resultPrompt: null,
  });
};

const removeReference = (id) => {
  references.value = references.value.filter(ref => ref.id !== id);
};

const analyzeReference = async (id) => {
  const reference = references.value.find(ref => ref.id === id);

  if (!reference.imageFile || !reference.annotation || !reference.annotationDescription) {
    alert("Please complete all fields!");
    return;
  }

  reference.isLoading = true;

  const formData = new FormData();
  formData.append("image", reference.imageFile);
  formData.append("annotation", reference.annotation);
  formData.append("annotationDetail", reference.annotationDescription);


  try {
    const response = await fetch("http://127.0.0.1:8012/generate", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    console.log("Server Response:", data);
    reference.resultPrompt = data.prompt
  } catch (error) {
    console.error("Error submitting data:", error);
  }


  reference.isLoading = false;



};


</script>



<template>

    <div class="w-full flex flex-col justify-center items-center pt-[60px] pb-64">
        
        <div class="w-4/5 flex flex-col justify-start items-center border border-neutral-300 rounded-lg mt-16 p-8">
          

          <h1 class="text-black text-3xl my-8 font-standard">
              Generate Image 
          </h1>

          <!-- OG PROMPT -->
          <div class="w-full my-8">
            <p class="text-black my-4 font-bold">Original prompt (Optional)</p>
            <textarea
              v-model="replicateText"
              placeholder="Enter your existing prompt here or leave empty"
              class="w-full  border border-neutral-300 rounded-lg text-black p-4"
            ></textarea>
          </div>

          <div class="w-full flex flex-col justify-start items-center border border-neutral-300 border-1 my-8 h-[1px]">
          </div>


          <p class="text-black my-4 font-bold w-full">Reference Images</p>

          <!-- IMAGE UPLOAD -->
          <div class="w-full flex flex-row justify-start my-8 flex-wrap">



            <ImageBox 
              v-for="reference in references" 
              :key="reference.id" 
              v-model="references"
              :reference="reference"
              @remove="removeReference"
              @analyze="analyzeReference"
              @updateImage="updateImage(reference.id, $event)"
              class="w-[30%] mr-[3%]"
            />

          </div>

          <Button title="Add Reference" :icon="'i-heroicons-plus'" :style="'white'" class="my-2" @click="addReference"/>

          <div class="w-full flex flex-col justify-start items-center border border-neutral-300 border-1 my-8 h-[1px]">
          </div>
          <div class="w-full my-8">

            <p class="text-black my-4 font-bold">Generated Prompt Pieces</p>
          </div>

          <template v-for="reference in references" :key="reference.id">
            <PromptBox 
              v-if="reference && reference.resultPrompt" 
              :content="reference.resultPrompt" 
              color="teal" 
              class="w-full my-4"
            />
          </template>

          <Button title="Generate Final Prompt" :icon="'i-heroicons-arrow-right-20-solid'" :style="'white'" class="my-12" @click="generatePrompt" :loading="isLoading"/>

          <div class="w-full my-8">

            <p class="text-black my-4 font-bold">Final Prompt</p>
            <PromptBox color="orange" v-if="generatedPrompt" :content="generatedPrompt" class="w-full"/>

          </div>

          <!-- 
          <div class="w-full my-8">
            <p class="text-black my-4">2. What you want to replicate?</p>
            <textarea
              v-model="replicateText"
              placeholder="Write description"
              class="w-full h-32 border border-black rounded-lg text-black p-4"
            ></textarea>
          </div>

          <div class="w-full my-8">
            <p class="text-black my-4">3. What you want to add?</p>
            <textarea
              v-model="addText"
              placeholder="Write description"
              class="w-full h-32 border border-black rounded-lg text-black p-4"
            ></textarea>
          </div>



 -->
         


        </div>


    </div>

</template>