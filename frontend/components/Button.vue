<script setup lang="ts">

    const props = defineProps(['title', 'icon', 'loading'])


</script>





<template>

    <div class="justify-between flex-shrink-0 font-medium  gap-x-2.5  py-2 px-1.5  md:py-2.5 shadow-sm bg-black hover:bg-gray-500 dark:disabled:bg-white focus-visible:ring-inset focus-visible:ring-1 focus-visible:ring-primary-500 dark:focus-visible:ring-primary-400 inline-flex items-center cursor-pointer ring-1 px-3 relative overflow-hidden rounded-full">


        <p  class="cursor-pointer flex-1  font-light text-base text-center">
            {{title}}   
        </p>
        
        <UIcon v-if="icon !== undefined" class="flex-shrink-0 h-6 w-6" :name="icon" dynamic/>


        <div v-if="loading" class="absolute top-0 left-0 w-full h-full bg-white"></div>
        <div v-if="loading" class="absolute top-0 left-0 w-full h-full loading-anim bg-black"></div>

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


