<template>
  <div class="h-full w-full">

    <ErrorHandler></ErrorHandler>
    <slot></slot>
  </div>
</template>


<style>
html,
body {
  @apply h-full w-full;
}

@media (prefers-color-scheme: light) {

  div#__nuxt,
  #__layout,
  #__layout>div,
  #app {
    /* background-size: 40px 40px;
      background-image:
        linear-gradient(to right, grey 1px, transparent 1px),
        linear-gradient(to bottom, grey 1px, transparent 1px); */
    @apply h-full w-full bg-white;
    /* mask-image: linear-gradient(0deg, #fff, rgba(255, 255, 255, 0.6)); */
  }
}


@media (prefers-color-scheme: dark) {

  div#__nuxt,
  #__layout,
  #__layout>div,
  #app {
    @apply h-full w-full;
  }
}
</style>