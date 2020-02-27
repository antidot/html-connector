/*
 File: language-dropdown-button.js */
(window.webpackJsonp=window.webpackJsonp||[]).push([[133],{1608:function(b,f,a){function d(a){return a&&a.__esModule?a:{default:a}}var e,c;b=(e="\n   position: absolute;\n   right: -{;\n   margin-top: {;\n   font-size: {;\n   border-radius: {;\n\n   opacity: {;\n   transform: {;\n   transition: opacity 0.2s linear,\n      transform 0.2s ease-in-out;\n".split("{"),c="\n   position: absolute;\n   right: -{;\n   margin-top: {;\n   font-size: {;\n   border-radius: {;\n\n   opacity: {;\n   transform: {;\n   transition: opacity 0.2s linear,\n      transform 0.2s ease-in-out;\n".split("{"),
Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(c)}})));var k=d(a(0));e=d(a(1));c=a(2);var h=a(22);f=d(a(467));a=a(4).constants.fontSize;var g=(0,e.default)(f.default)(b,c.space[4],c.space[3],a[1],c.borderRadius.lg,function(a){return a.isOpen?1:0},function(a){return a.isOpen?"translateY(0)":"translateY(-1.5rem)"});window.languageDropdownButton=new function l(){var a=this;if(!(this instanceof l))throw new TypeError("Cannot call a class as a function");!0;this.setProps=function(b){return a.props=
b};this.setRenderTarget=function(b){return a.renderTarget=b};this.toggle=function(b){ga(App.which+".send","event","Header","Language","click");a.isOpen=!a.isOpen;a.isOpen?a.showDropdown(b):a.hideDropdown(b,!0)};this.showDropdown=function(b){b.stop();a.renderTarget.classList.remove("invisible");document.addEventListener("click",a.hideDropdown);a.renderDropdown()};this.hideDropdown=function(b){!(1<arguments.length&&void 0!==arguments[1]&&arguments[1])&&a.renderTarget.contains(b.target)||(a.isOpen=!1,
a.renderDropdown(),document.removeEventListener("click",a.hideDropdown),setTimeout(function(){return a.renderTarget.classList.add("invisible")},150))};this.renderDropdown=function(){var b=a.props,m=b.languages,q=b.translationPreferencesUrl,c=b.machineTranslationEnabled;b=b.machineTranslationRequested;(0,h.render)(k.default.createElement(g,{isOpen:a.isOpen,languages:m,translationPreferencesUrl:q,machineTranslationEnabled:c,machineTranslationRequested:b}),a.renderTarget)};this.isOpen=!1;this.renderTarget=
this.props=null}},230:function(b,f,a){b=this&&this.__makeTemplateObject||function(a,b){return Object.defineProperty?Object.defineProperty(a,"raw",{value:b}):a.raw=b,a};var d=this&&this.__importStar||function(a){if(a&&a.__esModule)return a;var b={};if(null!=a)for(var m in a)Object.hasOwnProperty.call(a,m)&&(b[m]=a[m]);return b.default=a,b},e=this&&this.__importDefault||function(a){return a&&a.__esModule?a:{default:a}};Object.defineProperty(f,"__esModule",{value:!0});var c,k,h,g=d(a(0));d=e(a(1));e=
a(2);var p=a(96);a=a(4).constants.fontSize;var l=d.default(p.CardLink)(c||(c=b("\n   margin: , 0px;\n\n   :hover \x3e .iso-code {\n      color: ,;\n      background-color: ,;\n      border-color: ,;\n   }\n\n   :hover \x3e .language-name {\n      color: ,;\n   }\n".split(","),"\n   margin: , 0px;\n\n   :hover \x3e .iso-code {\n      color: ,;\n      background-color: ,;\n      border-color: ,;\n   }\n\n   :hover \x3e .language-name {\n      color: ,;\n   }\n".split(","))),e.space[2],function(a){return a.theme.isoCode.hover.font},
function(a){return a.theme.isoCode.hover.background},function(a){return a.theme.isoCode.hover.border},function(a){return a.theme.languageNameHover}),r=d.default.div(k||(k=b('\n   display: flex;\n   color: {;\n   background-color: {;\n   line-height: inherit;\n   font-size: {;\n   font-family: "Overpass Mono", monospace;\n   margin-right: {;\n   padding: 1px 4px;\n   border: 1px solid\n      {;\n   border-radius: {;\n'.split("{"),'\n   display: flex;\n   color: {;\n   background-color: {;\n   line-height: inherit;\n   font-size: {;\n   font-family: "Overpass Mono", monospace;\n   margin-right: {;\n   padding: 1px 4px;\n   border: 1px solid\n      {;\n   border-radius: {;\n'.split("{"))),
function(a){var b=a.theme;return a.isSelected?b.isoCode.selected.font:b.isoCode.standard.font},function(a){var b=a.theme;return a.isSelected?b.isoCode.selected.background:"transparent"},a[0],e.space[4],function(a){var b=a.theme;return a.isSelected?b.isoCode.selected.border:b.isoCode.standard.border},e.borderRadius.sm),t=d.default.div(h||(h=b(["\n   display: flex;\n   color: ",";\n   line-height: inherit;\n"],["\n   display: flex;\n   color: ",";\n   line-height: inherit;\n"])),function(a){return a.theme.languageName});
f.default=function(a){var b=a.language,c=a.onClickLanguage;a=b.isoCode;var e=b.autoglottonym;b=b.isSelected;var d=a.toLowerCase(),h=g.useCallback(function(){return c(d)},[c,d]);return g.default.createElement(l,{href:"#","data-langid":d,onClick:h},g.default.createElement(r,{className:"iso-code",isSelected:b},a),g.default.createElement(t,{className:"language-name"},e))}},231:function(b,f,a){Object.defineProperty(f,"__esModule",{value:!0});var d=Object.assign||function(a){for(var b=1;b<arguments.length;b++){var c=
arguments[b],d;for(d in c)Object.prototype.hasOwnProperty.call(c,d)&&(a[d]=c[d])}return a},e=a(0),c=e&&e.__esModule?e:{default:e};f.default=function(a){return function(b){var g=(0,e.createRef)(),f=(0,e.createRef)();return c.default.createElement(c.default.Fragment,null,c.default.createElement(a,d({},b,{onClickLanguage:function(a){f.current.value=a;CSRF.recheckAll();g.current.submit()}})),c.default.createElement("form",{ref:g,method:"POST",action:b.translationPreferencesUrl},c.default.createElement("input",
{ref:f,type:"hidden",name:"langid",value:""})))}}},232:function(b,f,a){Object.defineProperty(f,"__esModule",{value:!0});var d,e=(d=a(0))&&d.__esModule?d:{default:d},c=a(1);b=a(2);var k={background:b.color.white,isoCode:{standard:{font:b.color.gray6,border:b.color.gray3},hover:{font:b.color.white,background:b.color.blueLight1,border:b.color.blueLight1},selected:{font:b.color.gray1,background:b.color.blue,border:b.color.blue}},languageName:b.color.gray6,languageNameHover:b.color.gray5,machineTranslation:b.color.gray6,
machineTranslationBorder:b.color.gray2},h={background:"#222222",isoCode:{standard:{font:b.color.gray3,border:b.color.gray6},hover:{font:b.color.gray8,background:b.color.gray1,border:b.color.gray1},selected:{font:b.color.gray8,background:b.color.gray4,border:b.color.gray4}},languageName:b.color.gray3,languageNameHover:b.color.white,machineTranslation:b.color.gray2,machineTranslationBorder:"#3D3D3D"};f.default=function(a){return e.default.createElement(c.ThemeProvider,{theme:a.isLightTheme?k:h},a.children)}},
467:function(b,f,a){var d;b=this&&this.__makeTemplateObject||function(a,b){return Object.defineProperty?Object.defineProperty(a,"raw",{value:b}):a.raw=b,a};var e=this&&this.__extends||(d=function(a,b){return(d=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(a,b){a.__proto__=b}||function(a,b){for(var c in b)b.hasOwnProperty(c)&&(a[c]=b[c])})(a,b)},function(a,b){function c(){this.constructor=a}d(a,b);a.prototype=null===b?Object.create(b):(c.prototype=b.prototype,new c)}),c=this&&this.__importDefault||
function(a){return a&&a.__esModule?a:{default:a}};Object.defineProperty(f,"__esModule",{value:!0});var k,h=c(a(0)),g=c(a(1)),p=a(2),l=c(a(230)),r=c(a(231)),t=c(a(232)),m=c(a(468)),q=a(96),n=g.default(q.CardColumn)(k||(k=b(["\n   padding-right: ",";\n"],["\n   padding-right: ",";\n"])),p.space[6]),u=r.default(function(a){var b=a.rightColumn,c=a.onClickLanguage;return h.default.createElement(q.CardColumnContainer,null,h.default.createElement(n,null,a.leftColumn.map(function(a){return h.default.createElement(l.default,
{key:a.isoCode,language:a,onClickLanguage:c})})),h.default.createElement(q.CardColumn,null,b.map(function(a){return h.default.createElement(l.default,{key:a.isoCode,language:a,onClickLanguage:c})})))});a=function(a){function b(b){return a.call(this,b)||this}return e(b,a),b.prototype.render=function(){var a=this.props,b=a.className,c=(a.children,a.languages),d=a.translationPreferencesUrl,e=a.machineTranslationEnabled,f=a.machineTranslationRequested;a=a.isLightTheme;for(var g=[],k=[],n=0;n<c.length;n++)0==
n%2?g.push(c[n]):k.push(c[n]);return h.default.createElement(t.default,{isLightTheme:a},h.default.createElement(q.DropdownContainer,{className:b},h.default.createElement(u,{leftColumn:g,rightColumn:k,translationPreferencesUrl:d}),e&&h.default.createElement(m.default,{translationPreferencesUrl:d,machineTranslationRequested:f})))},b}(h.default.Component);f.default=a},468:function(b,f,a){var d;b=this&&this.__makeTemplateObject||function(a,b){return Object.defineProperty?Object.defineProperty(a,"raw",
{value:b}):a.raw=b,a};var e=this&&this.__extends||(d=function(a,b){return(d=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(a,b){a.__proto__=b}||function(a,b){for(var c in b)b.hasOwnProperty(c)&&(a[c]=b[c])})(a,b)},function(a,b){function c(){this.constructor=a}d(a,b);a.prototype=null===b?Object.create(b):(c.prototype=b.prototype,new c)}),c=this&&this.__importDefault||function(a){return a&&a.__esModule?a:{default:a}};Object.defineProperty(f,"__esModule",{value:!0});var k,h,g=c(a(0));
c=c(a(1));var p=a(2),l=a(8),r=c.default.div(k||(k=b(["\n   display: flex;\n   justify-content: space-between;\n   padding: "," ",";\n   color: ",";\n   border-top: 1px solid ",";\n;\n"],["\n   display: flex;\n   justify-content: space-between;\n   padding: "," ",";\n   color: ",";\n   border-top: 1px solid ",";\n;\n"])),p.space[5],p.space[6],function(a){return a.theme.machineTranslation},function(a){return a.theme.machineTranslationBorder}),t=c.default.span(h||(h=b(["\n   font-weight: bold;\n"],["\n   font-weight: bold;\n"])));
a=function(a){function b(b){var c=a.call(this,b)||this;return c.state={machineTranslationRequested:c.props.machineTranslationRequested},c.onToggleMachineTranslation=function(){c.setState({machineTranslationRequested:!c.state.machineTranslationRequested},function(){CSRF.recheckAll();c.machineTranslationForm.current.submit()})},c.machineTranslationForm=g.default.createRef(),c}return e(b,a),b.prototype.render=function(){var a=this.state.machineTranslationRequested;return g.default.createElement("form",
{ref:this.machineTranslationForm,method:"POST",action:this.props.translationPreferencesUrl},g.default.createElement(r,null,g.default.createElement(t,null,_js("Machine Translation")),g.default.createElement(l.Toggle,{checked:a,label:a?_js("On"):_js("Off"),onChange:this.onToggleMachineTranslation})),g.default.createElement("input",{type:"hidden",name:"langid",value:""}),g.default.createElement("input",{type:"hidden",name:"machineTranslate",value:a?"on":""}))},b}(g.default.Component);f.default=a},96:function(b,
f,a){function d(a,b){return Object.freeze(Object.defineProperties(a,{raw:{value:Object.freeze(b)}}))}Object.defineProperty(f,"__esModule",{value:!0});f.CardLink=f.CardColumn=f.CardColumnContainer=f.DropdownContainer=void 0;var e;b=d(["\n   display: flex;\n   flex-direction: column;\n   background-color: ",";\n   box-shadow: ",";\n"],["\n   display: flex;\n   flex-direction: column;\n   background-color: ",";\n   box-shadow: ",";\n"]);var c=d(["\n   display: flex;\n   padding: "," ",";\n"],["\n   display: flex;\n   padding: ",
" ",";\n"]),k=d(["\n   display: flex;\n   flex-flow: column nowrap;\n"],["\n   display: flex;\n   flex-flow: column nowrap;\n"]),h=d(["\n   display: flex;\n   align-items: center;\n   line-height: ",";\n   font-weight: ",";\n   white-space: nowrap;\n\n   :hover {\n      background-color: transparent !important;\n      text-decoration: none;\n   }\n"],["\n   display: flex;\n   align-items: center;\n   line-height: ",";\n   font-weight: ",";\n   white-space: nowrap;\n\n   :hover {\n      background-color: transparent !important;\n      text-decoration: none;\n   }\n"]),
g=(e=a(1))&&e.__esModule?e:{default:e};e=a(8);a=a(2);f.DropdownContainer=g.default.div(b,function(a){return a.theme.background},e.constants.shadows.dropShadow[2]);f.CardColumnContainer=g.default.div(c,a.space[5],a.space[6]);f.CardColumn=g.default.div(k);f.CardLink=g.default.a(h,a.space[3],a.fontWeight.bold)}},[[1608,0,1]]]);