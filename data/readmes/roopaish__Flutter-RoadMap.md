# [Flutter RoadMap](https://flutter-roadmap.netlify.app/#/) 

## Contents

- [Flutter Notes](#notes)
- [Quiz App](https://flutter-roadmap.netlify.app/#/quiz-app)
- [Personal Expense App](https://flutter-roadmap.netlify.app/#/expense-app)
- [Meals App](https://flutter-roadmap.netlify.app/#/meals-app)
- [Shop App](https://flutter-roadmap.netlify.app/#/shop-app)
- [Great Places App](https://flutter-roadmap.netlify.app/#/great-places-app)
- [Chat App](https://flutter-roadmap.netlify.app/#/chat-app)

## Index

## 1

[Flutter Basics(Quiz App)](#flutter-basicsquiz-app)

- [Command Line Tools](#command-line-tools)
- [Files and Folder Structure](#files-and-folder-structure)
- [Dart and Flutter](#dart-and-flutter)
  > Data Types, Function, Operators, Class, Constructor, Maps, List, ...spread operator, const vs final, getter, string interpolation, String methods, Parsing etc.
- [Analyze main.dart](#analyze-maindart)
- [Widgets](#widgets)
  > MaterialApp, Scaffold, Text, Row, Column, ElevatedButton, TextButton, OutlinedButton
- [Stateless vs Stateful Widget](#stateless-vs-stateful-widget)
- [Github Workflow | Build for Web automatically](#github-workflow--build-for-web-automatically)
- [Adding Custom Assets | Media | Fonts](#adding-custom-assets--media--fonts)

## 2

[More Widgets, Styling, Adding Logic(Personal Expense App)](#more-widgets-styling-adding-logicpersonal-expense-app)

- [App/Page Widgets](#apppage-widgets)
- [Layout Widgets | Container | Row | Column](#layout-widgets--container--row--column)
- [Responsive Widgets | FractionallySizedBox | Flexible | FittedBox | Expanded](#responsive-widgets--fractionallysizedbox--flexible--fittedbox--expanded)
- [Content Containers | Stack | Card](#content-containers--stack--card)
- [Repeat Elements Widgets | ListView | GridView](#repeat-elements-widgets--listview--gridview)
- [Content Type Widgets | Text | Image | Icon](#content-type-widgets--text--image--icon)
- [User Input Widgets | TextField | Buttons | GestureDetector | InkWell](#user-input-widgets--textfield--buttons--gesturedetector--inkwell)
- [ThemeData | SizedBox | Divider | CircleAvatar | ClipRRect | Switch](#themedata--sizedbox--divider--circleavatar--cliprrect--switch)
- [Flutter Methods to show Widgets](#flutter-methods-to-show-widgets)
- [Access methods of StatefulWidget from State Widget](#access-methods-of-statefulwidget-from-state-widget)
- [List/Map Methods | Switch-Case](#listmap-methods--switch-case)

## 3

[Responsive and Adaptive UI(Personal Expense App)](#responsive-and-adaptive-uipersonal-expense-app)

- [Get Device Screen Size | Media Query](#get-device-screen-size--media-query)
- [Orientation | Portrait | Landscape](#orientation--portrait--landscape)
- [Know Size given to a specific Widget | LayoutBuilder](#know-size-given-to-a-specific-widget--layoutbuilder)
- [UI based on Platform | Adaptive UI](#ui-based-on-platform--adaptive-ui)

## 4

[Flutter Internals and Performance](#flutter-internals-and-performance)

- [Flutter Under the Hood](#flutter-under-the-hood)
- [Avoid unnecessary Widget rebuild](#avoid-unnecessary-widget-rebuild)
- [Extracting Widgets](#extracting-widgets)
- [Widget Lifecycle | initState | didUpdateWidget | dispose | didChangeDependencies](#widget-lifecycle--initstate--didupdatewidget--dispose--didchangedependencies)
- [App Lifecycle](#app-lifecycle)
- [Context](#context)
- [Key | Solve List State Problems](#key--solve-list-state-problems)

## 5

[Navigation and Multiple Screens(Meals App)](#navigation-and-multiple-screensmeals-app)

- [Gradient](#gradient)
- [Navigator](#navigator)
- [NavigationBar at Top | TabBar](#navigationbar-at-top--tabbar)
- [BottomNavigationBar](#bottomnavigationbar)
- [Drawer](#drawer)
- [Stack of Pages](#stack-of-pages)
- [ListTile with trailing Switch | SwitchListTile](#listtile-with-trailing-switch--switchlisttile)
- [Pass Data through Route](#pass-data-through-route)

## 6

[State Management(Shop App)](#state-managementshop-app)

- [Problem with passing Data through 

[...截断...]

Routes](#problem-with-passing-data-through-routes)
- [State Management | Provider](#state-management--provider)
- [Inheritance(extends) vs Mixins(with)](#inheritanceextends-vs-mixinswith)
- [Creating provider for a List of items | Provider Constructors](#creating-provider-for-a-list-of-items--provider-constructors)
- [Using Consumer instead of Provider](#using-consumer-instead-of-provider)
- [PopupMenuButton](#popupMenuButton)
- [Some Map Methods](#some-map-methods)
- [Using multiple Providers | MultiProvider](#using-multiple-providers--multiprovider)
- [Resolve Collision of same Class Name from different imports](#resolve-collision-of-same-class-name-from-different-imports)
- [Slide-to-delete | Dismissible Widget](#slide-to-delete--dismissible-widget)

## 7

[User Inputs and Forms(Shop App)](#user-inputs-and-formsshop-app)

- [Popup that slides from Bottom | Snackbar](#popup-that-slides-from-bottom--snackbar)
- [AlertDialog](#alertdialog)
- [Forms](#forms)
- [Image Previewer](#image-previewer)
- [Saving and Validating Form](#saving-and-validating-form)

## 8

[Sending HTTP Requests(Shop App)](#sending-http-requestsshop-app)

- [Setting up Firebase Realtime Database](#setting-up-firebase-realtime-database)
- [How to Send http Requests](#how-to-send-http-requests)
- [Sending data (POST)](#sending-data-post)
- [Future and Async | try-catch](#future-and-async-code--try-catch)
- [Fetching Data (GET)](#fetching-data-get)
- [Pull-to-Refresh | RefreshIndicator](#pull-to-refresh--refreshindicator)
- [Updating(PATCH) & Deleting(DELETE) Data](#updatingpatch-&-Deletingdelete-data)
- [Fetch Data every time the State changes | FutureBuilder](#fetch-data-every-time-the-state-changes--futurebuilder)

## 9

[Authentication(Shop App)](#authenticationshop-app)

- [How Authentication works](#how-authentication-works)
- [Firebase Real Time Database Rules](#firebase-real-time-database-rules)
- [User SignUp/SignIn | Firebase Auth REST API](#user-signupsignin--firebase-auth-rest-api)
- [Handling Authentication Error](#handling-authentication-error)
- [Storing Token Locally | Memory](#storing-token-locally--memory)
- [Passing Provider as arguments to Another Provider | ChangeNotifierProxyProvider](#passing-provider-as-arguments-to-another-provider--changenotifierproxyprovider)
- [Setting Favorite Status per User](#setting-favorite-status-per-user)
- [Filtering Products by Creator](#filtering-products-by-creator)
- [Logout Manually/Automatically when Token expires](#logout-manuallyautomatically-when-token-expires)
- [Auto-login Users | Shared Preferences](#auto-login-users--shared-preferences)

## 10

[Animations(Shop App)](#animationsshop-app)

- [Manually Controlled Animation](#manually-controlled-animation)
- [AnimatedBuilder](#animatedbuilder)
- [AnimatedContainer](#animatedcontainer)
- [CurvedAnimation | FadeTransition | SlideTransition | FadeInImage | Hero](#curvedanimation--fadetransition--slidetransition--fadeinimage--hero)
- [Fancy Scrolling | Slivers](#fancy-scrolling--slivers)
  > When scrolled, the image at top will gradually become smaller, until it transforms into an appBar with given title
- [Custom Route Transition](#custom-route-transition)

## 11

[Using Native Device Features like Camera, Maps, Location(Great Places App)](#using-native-device-features-like-camera-maps-locationgreat-places-app)

- [Place Class](#place-class)
- [Taking A Photo | ImagePicker](#taking-a-photo--imagepicker)
- [Storing Image on Memory | Copy File](#storing-image-on-memory--copy-file)
- [Storing Image in Filesystem using SQLlite](#storing-image-in-filesystem-using-sqllite)
- [Taking Current Location as Input](#taking-current-location-as-input)
- [Entering Custom Location](#entering-custom-location)
- [Saving location to SQLite](#saving-location-to-sqlite)

## 12

[Firebase, Image Upload, Push Notifications(Chat App)](#firebase-image-upload-push-notificationschat-app)

- [Firebase SDK Setup](#firebase-sdk-setup)
- [Rendering Firestore data with StreamBuilde