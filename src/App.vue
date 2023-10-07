<template>
  <v-app id="inspire">
    <div class="navBar">
      <v-navigation-drawer v-model="drawer">
        <!-- v-navigation-drawerはサイドバーの設定 -->
        <v-label for="file_photo">
          画像のアップロード
          <input type="file" id="file_photo" @change="handleFilename" style="display: none" />
        </v-label>
        <v-label>
          フォルダのアップロード
          <input type="file" id="file_photo" @change="handleFolderName" style="display: none" webkitdirectory/>
        </v-label>
      </v-navigation-drawer>
      
      <v-app-bar>
        <v-app-bar-nav-icon @click="drawer = !drawer"><span class="navIcon">≡</span></v-app-bar-nav-icon>
        <v-toolbar-title>shinkenote</v-toolbar-title>
      </v-app-bar>
    </div>
    
    <v-main>
      <v-container>
        <v-row>
          <!-- input size小さくすると形崩れる -->
          <input type="text" v-model="filterName" class="filterCss" placeholder="画像を検索" />
          <v-col v-for="file in filesFilter" :key="file.id" cols="4">
            <button v-if="file.star" @click="removeFavs(file)">★</button>
            <button v-if="!file.star" @click="addToFavs(file)">☆</button>
            <v-card height="200" width="200" class="card">
              <img
              :src="`${file.url}`"
              alt=""
              style="object-fit: contain; max-width: 200px; max-height: 200px"
              />
            </v-card>
            <p class="photoDesc">{{ file.name.replace(/\.(png|jpe?g|bmp)$/, "") }}</p>
            <!-- <button class="deleteButton" @click="removeFilename(file)">削除</button> -->
            <!-- 現状削除ボタンを使う意味がない -->
          </v-col>
        </v-row>
      </v-container>
      <v-btn @click="test">テスト(未設定)</v-btn>
    </v-main>
  </v-app>
  <header>
  </header>
    
  <RouterView />
</template>

<script>
import { RouterLink, RouterView } from 'vue-router'
import axios from "axios";
let id = 0

export default {
  data() {
    return {
      drawer: null,
      files: [],
      filterName: '',
      isH: false,
      result: null,
    }
  },
  computed: {
    filesFilter() {
      return this.filterName.length < 1
        ? this.files
        : this.files.filter((e) => e.name.startsWith(this.filterName))
    },
  },
  mounted() {
    this.readFavs()
  },
  methods: {
    test() {
          axios.get('/')
            .then(response => {
              console.log(response)
            })
            .catch(error => {
              console.log('NO')
              console.log(error);
            })
          },
    handleFilename(event) {
      const url = URL.createObjectURL(event.target.files[0], {type: "image/png"});
      this.files.push({ id: id++, name: event.target.files[0].name, star: false, url: url, blob: event.target.files[0], key: null })
      event.target.value = ''
    },
    handleFolderName(event) {
      const file = event.target.files
      for (let i = 0; i < file.length; i++) {
        if (file[i].name.match(/\.ini$/)) {
          continue
        }
        console.log(file[i])
        // file[i]内のwebkitRelativePath
        const url = URL.createObjectURL(file[i], {type: "image/png"});
        console.log('url',url)  
        this.files.push({ id: id++, name: file[i].name, star: false, url: url, blob: file[i], key: null })
      }
      event.target.value = ''
    },
    removeFilename(name) {
      this.files = this.files.filter((t) => t !== name)
      // キャッシュが削除されないので使用しない
    },
    addToFavs(file) {
      console.log('file',file)
      const blob = file.blob
      const fileReader = new FileReader()
      fileReader.onload = async function () {
        const dataUrl = this.result
        const name = file.name
        const item = { name,dataUrl }
        const itemStr = JSON.stringify(item)
        const key = "item_" + new Date().getTime()
        const response = new Response(itemStr, {
          headers: {
            'Content-Type': 'application/json'
          }
        })
        const cache = await caches.open('items')
        cache.put(key, response)
        file.key = key
        file.star = !file.star
      }
      if(!blob) {
        console.log('blob = null')
        file.star = !file.star
      } else {
        fileReader.readAsDataURL(blob)
      }
    },
    async removeFavs(file) {
      const cache = await caches.open('items')
      console.log(file.key)
      await cache.delete(file.key)
      this.files = this.files.filter((t) => t !== file)
      // const keys = await cache.keys()
      // for (const key of keys) {
      //   const res = await cache.match(key)
      //   const item = await res.json()
      //   console.log(item)
      //   if (item.dataUrl === file.url) {
      //     await cache.delete()
      //     // this.files = this.files.filter(i => i !== item)
      //   }
      // }
      file.star = !file.star
      // cache.delete(file)
    },
    async readFavs() {
      const cache = await caches.open('items')
      const keys = await cache.keys()
      for (const key of keys) {
        const res = await cache.match(key)
        const item = await res.json()
        this.files.push({
          id: id++,
          name: item.name,
          star: true,
          url: item.dataUrl,
          blob: null,
          key: key.url.replace('http://localhost:5173/','')
        }) 
      }
    },
  }
}
</script>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }

  ul {
    list-style-type: none;
  }

  img {
    width: 300px;
    height: 300px;
    object-fit: contain;
    max-width: 80%;
  }

  label {
    color: white;
    background-color: green;
    padding: 32px;
    border-radius: 160px;
    cursor: pointer;
    opacity: 1.0;
    font-size: 16px;
    margin: 16px 16px 16px 6px;
  }

  .deleteButton {
    color: #999;
    padding-left: 8px;
    font-size: 0.95rem;
  }
  .deleteButton:hover {
    color: blue;
    opacity: 0.9;
  }

  .navBar {
    margin-bottom: 32px;
  }
  .navIcon {
    font-size: 24px;
    color: #333;
  }
  
  .filterCss {
    width: 100%; /*親要素いっぱい広げる*/
    padding: 10px 15px; /*ボックスを大きくする*/
    font-size: 16px;
    border-radius: 3px; /*ボックス角の丸み*/
    border: 2px solid #ddd; /*枠線*/
    box-sizing: border-box; /*横幅の解釈をpadding, borderまでとする*/
  }

  .photoDesc {
    font-size: 20px;
    padding: 8px;
  }

  .card {
    box-shadow: none;
  }
}
</style>
