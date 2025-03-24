<script setup lang="ts">
import { defineProps, defineEmits } from "vue";


const props = defineProps(['reference'])


const emit = defineEmits(["remove", "analyze", "updateImage"]);

const handleImageUpload = (event) => {
  const file = (event.target as HTMLInputElement).files?.[0]; // Get the uploaded file
  if (file) {
    const reader = new FileReader(); // Read the file as a data URL for preview
    reader.onload = () => {
      props.reference.selectedImage = reader.result as string;

      emit("updateImage", file);
    };
    reader.readAsDataURL(file); // Read the file
  }
};




</script>


<template>
    <div class="border border-neutral-300 rounded-lg p-4 ">
            
        <div 
          class="bg-neutral-100 rounded-lg flex justify-center items-center cursor-pointer hover:bg-neutral-300 overflow-hidden relative" 
          style="aspect-ratio: 1.62;"
        >
          <label class="absolute inset-0 flex justify-center items-center cursor-pointer">
            <input 
              type="file" 
              @change="handleImageUpload" 
              accept="image/*" 
              class="hidden"
            />
            <img 
              v-if="reference && reference.selectedImage" 
              :src="reference.selectedImage" 
              class="w-full h-full object-cover"
            />
            <span v-else class="text-black text-2xl">+</span>
          </label>
        </div>
        <p class="text-black my-4">
            What aspect are you referencing?
        </p>

        <USelect v-model="reference.annotation" :items="['Subject', 'Background', 'Style', 'Vibe', 'Lighting', 'View', 'Material', 'Customized']" class="w-full rounded-lg  my-4 px-4 py-2 flex flex-row items-center bg-white text-black cursor-pointer hover:bg-neutral-200" />


        <div 
          class="w-full overflow-hidden" 
          :class="reference.annotation === 'Customized' ? 'h-auto' : 'h-0'"
        >
          <textarea 
            v-model="reference.customAnnotation" 
            rows=1
            placeholder="Custom annotation" 
            class="w-full text-sm border border-neutral-800 rounded-lg text-black px-4 py-2 resize-none">
          </textarea> 
        </div>


        <div class="w-full">
          <p class="text-black my-4">Annotation Details</p>
          <textarea 
          v-model="reference.annotationDescription" 
          placeholder="Add your annotation" class="w-full border border-neutral-800 rounded-lg text-black px-4 py-2 resize-none"></textarea> 
        </div>


        <div class="w-full rounded-lg border border-neutral-800 my-4 p-2 flex flex-row items-center justify-between cursor-pointer bg-red-400 hover:bg-red-200" @click="emit('remove', reference.id)">
          <p class="text-black text-center w-full">Delete</p>
        </div>


        <div class="relative overflow-hidden w-full rounded-lg border border-neutral-800 mt-4 p-2 flex flex-row items-center justify-between cursor-pointer bg-blue-400 hover:bg-blue-200" @click="emit('analyze', reference.id)">


            <p class="text-black text-center w-full">
                Analyze
            </p>

            <div v-if="reference.isLoading" class="absolute top-0 left-0 w-full h-full bg-white"></div>
            <div v-if="reference.isLoading" class="absolute top-0 left-0 w-full h-full loading-anim bg-black"></div>


        </div>



    </div>  

</template>





<style type="text/css" scoped>

  .loading-button{
    transition: 0.5s ease; 
  }
  
  .loading-button .button-icon{
      position: absolute;
      right: 0%;
      top: 50%;
      transform: translate(0%, -50%);
      transition: 0.5s ease; 
      opacity: 0;
  }

  .loading-button:hover .button-icon{
      transform: translate(-10px, -50%);
      opacity: 1;
  }


  .loading-anim{
    animation: slide-right 2s linear infinite;  
  }

  @keyframes slide-right {
    from {
      transform: translateX(-100%);  
    }
    to {
      transform: translateX(100%); 
    }
  }

</style>




