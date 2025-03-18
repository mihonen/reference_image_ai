<script setup lang="ts">


</script>

<template>
    <div class="fixed backdrop-blur-md border-b border-neutral-500/40 flex justify-between lg:justify-center items-center px-4 bg-black" style="z-index: 10; width: 100%; flex-direction: row; height: 60px;">

        <div class="font-thin text-brand-600 flex  mr-4 flex-1  justify-start" >
            <div class="flex flex-row items-center ">

                <NuxtLink  :to="''" class="h-10 w-10">
                    <img :src="'https://neon-stack-storage.fra1.cdn.digitaloceanspaces.com/app_icons/icon_minimal.png'" alt="logo" class="h-10 w-10 lg:mr-2 hover:opacity-100" />
                </NuxtLink>


            </div>


        </div>


        <div class="flex flex-1 justify-end">
        <UIcon name="'i-heroicons-arrow-right-20-solid'" class="flex-shrink-0 h-6 w-6"/>

        </div>


    </div>
</template>








