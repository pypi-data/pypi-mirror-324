import{s as C,y as q,i as E,d as u,o as M,u as B,e as w,f as z,c as b,h as v,j as P,a as d,b as k,k as h,v as F,w as G,x as H,t as j,m as x,q as A}from"./scheduler.bDsl0G2p.js";import{S as J,i as K,t as D,b as I,c as L,a as N,m as O,d as Q}from"./index.DtyFm6kT.js";import"./0.D1YHP6Ug.js";import{T as R}from"./Trinket.DlhAoO-v.js";function U(r){let e,s,t,l,a,p,c,m;t=new R({props:{width:"50px",height:"35px",color:X}});const y=r[8].default,f=B(y,r,r[7],null);let o=r[0].length>=1&&T(r),i=r[1].length>=1&&V(r);return{c(){e=w("aside"),s=w("div"),L(t.$$.fragment),l=z(),a=w("div"),f&&f.c(),p=z(),o&&o.c(),c=z(),i&&i.c(),this.h()},l(n){e=b(n,"ASIDE",{monitor:!0,class:!0,style:!0});var _=v(e);s=b(_,"DIV",{style:!0});var S=v(s);N(t.$$.fragment,S),S.forEach(u),l=P(_),a=b(_,"DIV",{style:!0,class:!0});var g=v(a);f&&f.l(g),p=P(g),o&&o.l(g),c=P(g),i&&i.l(g),g.forEach(u),_.forEach(u),this.h()},h(){d(s,"style",r[3]),k(a,"padding","0 0 0 10px"),k(a,"margin","0"),k(a,"text-align","center"),d(a,"class","alert-message"),d(e,"monitor","problem alert"),d(e,"class","alert variant-filled-error"),d(e,"style",r[2])},m(n,_){E(n,e,_),h(e,s),O(t,s,null),h(e,l),h(e,a),f&&f.m(a,null),h(a,p),o&&o.m(a,null),h(a,c),i&&i.m(a,null),m=!0},p(n,_){(!m||_&8)&&d(s,"style",n[3]),f&&f.p&&(!m||_&128)&&F(f,y,n,n[7],m?H(y,n[7],_,null):G(n[7]),null),n[0].length>=1?o?o.p(n,_):(o=T(n),o.c(),o.m(a,c)):o&&(o.d(1),o=null),n[1].length>=1?i?i.p(n,_):(i=V(n),i.c(),i.m(a,null)):i&&(i.d(1),i=null),(!m||_&4)&&d(e,"style",n[2])},i(n){m||(D(t.$$.fragment,n),D(f,n),m=!0)},o(n){I(t.$$.fragment,n),I(f,n),m=!1},d(n){n&&u(e),Q(t),f&&f.d(n),o&&o.d(),i&&i.d()}}}function T(r){let e,s;return{c(){e=w("p"),s=j(r[0]),this.h()},l(t){e=b(t,"P",{style:!0});var l=v(e);s=x(l,r[0]),l.forEach(u),this.h()},h(){k(e,"font-weight","bold"),k(e,"word-wrap","anywhere")},m(t,l){E(t,e,l),h(e,s)},p(t,l){l&1&&A(s,t[0])},d(t){t&&u(e)}}}function V(r){let e,s;return{c(){e=w("p"),s=j(r[1])},l(t){e=b(t,"P",{});var l=v(e);s=x(l,r[1]),l.forEach(u)},m(t,l){E(t,e,l),h(e,s)},p(t,l){l&2&&A(s,t[1])},d(t){t&&u(e)}}}function W(r){let e,s,t=r[4]===!0&&U(r);return{c(){t&&t.c(),e=q()},l(l){t&&t.l(l),e=q()},m(l,a){t&&t.m(l,a),E(l,e,a),s=!0},p(l,[a]){l[4]===!0&&t.p(l,a)},i(l){s||(D(t),s=!0)},o(l){I(t),s=!1},d(l){l&&u(e),t&&t.d(l)}}}let X="#000000";function Y(r,e,s){let{$$slots:t={},$$scope:l}=e,{text:a=""}=e,{text_2:p=""}=e,{show:c="no"}=e,{size:m="regular"}=e;M(()=>{});let y=typeof a=="string"&&a.length>=1||c==="yes",f=`
	display: flex; 
	flex-direction: row;
	align-items: center;
	
	padding: 12px; 
	margin: 8px 0;
`,o="";return m==="small"&&(f=`
		display: flex; 
		flex-direction: row;
		align-items: center;
		
		padding: 4px; 
	`,o=`
		transform: scale(0.7)
	`),r.$$set=i=>{"text"in i&&s(0,a=i.text),"text_2"in i&&s(1,p=i.text_2),"show"in i&&s(5,c=i.show),"size"in i&&s(6,m=i.size),"$$scope"in i&&s(7,l=i.$$scope)},[a,p,f,o,y,c,m,l,t]}class le extends J{constructor(e){super(),K(this,e,Y,W,C,{text:0,text_2:1,show:5,size:6})}}export{le as P};
//# sourceMappingURL=Problem.D2rUnZta.js.map
