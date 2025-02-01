var ll = (n) => {
  throw TypeError(n);
};
var ol = (n, e, t) => e.has(n) || ll("Cannot " + t);
var rn = (n, e, t) => (ol(n, e, "read from private field"), t ? t.call(n) : e.get(n)), al = (n, e, t) => e.has(n) ? ll("Cannot add the same private member more than once") : e instanceof WeakSet ? e.add(n) : e.set(n, t), rl = (n, e, t, i) => (ol(n, e, "write to private field"), i ? i.call(n, t) : e.set(n, t), t);
new Intl.Collator(0, { numeric: 1 }).compare;
async function ia(n, e) {
  return n.map(
    (t) => new la({
      path: t.name,
      orig_name: t.name,
      blob: t,
      size: t.size,
      mime_type: t.type,
      is_stream: e
    })
  );
}
class la {
  constructor({
    path: e,
    url: t,
    orig_name: i,
    size: l,
    blob: o,
    is_stream: a,
    mime_type: s,
    alt_text: r,
    b64: f
  }) {
    this.meta = { _type: "gradio.FileData" }, this.path = e, this.url = t, this.orig_name = i, this.size = l, this.blob = t ? void 0 : o, this.is_stream = a, this.mime_type = s, this.alt_text = r, this.b64 = f;
  }
}
typeof process < "u" && process.versions && process.versions.node;
var Et;
class Vf extends TransformStream {
  /** Constructs a new instance. */
  constructor(t = { allowCR: !1 }) {
    super({
      transform: (i, l) => {
        for (i = rn(this, Et) + i; ; ) {
          const o = i.indexOf(`
`), a = t.allowCR ? i.indexOf("\r") : -1;
          if (a !== -1 && a !== i.length - 1 && (o === -1 || o - 1 > a)) {
            l.enqueue(i.slice(0, a)), i = i.slice(a + 1);
            continue;
          }
          if (o === -1)
            break;
          const s = i[o - 1] === "\r" ? o - 1 : o;
          l.enqueue(i.slice(0, s)), i = i.slice(o + 1);
        }
        rl(this, Et, i);
      },
      flush: (i) => {
        if (rn(this, Et) === "")
          return;
        const l = t.allowCR && rn(this, Et).endsWith("\r") ? rn(this, Et).slice(0, -1) : rn(this, Et);
        i.enqueue(l);
      }
    });
    al(this, Et, "");
  }
}
Et = new WeakMap();
const {
  SvelteComponent: oa,
  append_hydration: Ue,
  attr: Wt,
  children: Vt,
  claim_element: Gt,
  claim_space: Oi,
  claim_text: fn,
  detach: yt,
  element: jt,
  init: aa,
  insert_hydration: bo,
  noop: sl,
  safe_not_equal: ra,
  set_data: ri,
  set_style: wi,
  space: Ri,
  text: un,
  toggle_class: fl
} = window.__gradio__svelte__internal, { onMount: sa, createEventDispatcher: fa, onDestroy: ua } = window.__gradio__svelte__internal;
function ul(n) {
  let e, t, i, l, o = Rn(
    /*file_to_display*/
    n[2]
  ) + "", a, s, r, f, _ = (
    /*file_to_display*/
    n[2].orig_name + ""
  ), d;
  return {
    c() {
      e = jt("div"), t = jt("span"), i = jt("div"), l = jt("progress"), a = un(o), r = Ri(), f = jt("span"), d = un(_), this.h();
    },
    l(c) {
      e = Gt(c, "DIV", { class: !0 });
      var u = Vt(e);
      t = Gt(u, "SPAN", {});
      var h = Vt(t);
      i = Gt(h, "DIV", { class: !0 });
      var v = Vt(i);
      l = Gt(v, "PROGRESS", { style: !0, max: !0, class: !0 });
      var T = Vt(l);
      a = fn(T, o), T.forEach(yt), v.forEach(yt), h.forEach(yt), r = Oi(u), f = Gt(u, "SPAN", { class: !0 });
      var k = Vt(f);
      d = fn(k, _), k.forEach(yt), u.forEach(yt), this.h();
    },
    h() {
      wi(l, "visibility", "hidden"), wi(l, "height", "0"), wi(l, "width", "0"), l.value = s = Rn(
        /*file_to_display*/
        n[2]
      ), Wt(l, "max", "100"), Wt(l, "class", "svelte-cr2edf"), Wt(i, "class", "progress-bar svelte-cr2edf"), Wt(f, "class", "file-name svelte-cr2edf"), Wt(e, "class", "file svelte-cr2edf");
    },
    m(c, u) {
      bo(c, e, u), Ue(e, t), Ue(t, i), Ue(i, l), Ue(l, a), Ue(e, r), Ue(e, f), Ue(f, d);
    },
    p(c, u) {
      u & /*file_to_display*/
      4 && o !== (o = Rn(
        /*file_to_display*/
        c[2]
      ) + "") && ri(a, o), u & /*file_to_display*/
      4 && s !== (s = Rn(
        /*file_to_display*/
        c[2]
      )) && (l.value = s), u & /*file_to_display*/
      4 && _ !== (_ = /*file_to_display*/
      c[2].orig_name + "") && ri(d, _);
    },
    d(c) {
      c && yt(e);
    }
  };
}
function ca(n) {
  let e, t, i, l = (
    /*files_with_progress*/
    n[0].length + ""
  ), o, a, s = (
    /*files_with_progress*/
    n[0].length > 1 ? "files" : "file"
  ), r, f, _, d = (
    /*file_to_display*/
    n[2] && ul(n)
  );
  return {
    c() {
      e = jt("div"), t = jt("span"), i = un("Uploading "), o = un(l), a = Ri(), r = un(s), f = un("..."), _ = Ri(), d && d.c(), this.h();
    },
    l(c) {
      e = Gt(c, "DIV", { class: !0 });
      var u = Vt(e);
      t = Gt(u, "SPAN", { class: !0 });
      var h = Vt(t);
      i = fn(h, "Uploading "), o = fn(h, l), a = Oi(h), r = fn(h, s), f = fn(h, "..."), h.forEach(yt), _ = Oi(u), d && d.l(u), u.forEach(yt), this.h();
    },
    h() {
      Wt(t, "class", "uploading svelte-cr2edf"), Wt(e, "class", "wrap svelte-cr2edf"), fl(
        e,
        "progress",
        /*progress*/
        n[1]
      );
    },
    m(c, u) {
      bo(c, e, u), Ue(e, t), Ue(t, i), Ue(t, o), Ue(t, a), Ue(t, r), Ue(t, f), Ue(e, _), d && d.m(e, null);
    },
    p(c, [u]) {
      u & /*files_with_progress*/
      1 && l !== (l = /*files_with_progress*/
      c[0].length + "") && ri(o, l), u & /*files_with_progress*/
      1 && s !== (s = /*files_with_progress*/
      c[0].length > 1 ? "files" : "file") && ri(r, s), /*file_to_display*/
      c[2] ? d ? d.p(c, u) : (d = ul(c), d.c(), d.m(e, null)) : d && (d.d(1), d = null), u & /*progress*/
      2 && fl(
        e,
        "progress",
        /*progress*/
        c[1]
      );
    },
    i: sl,
    o: sl,
    d(c) {
      c && yt(e), d && d.d();
    }
  };
}
function Rn(n) {
  return n.progress * 100 / (n.size || 0) || 0;
}
function _a(n) {
  let e = 0;
  return n.forEach((t) => {
    e += Rn(t);
  }), document.documentElement.style.setProperty("--upload-progress-width", (e / n.length).toFixed(2) + "%"), e / n.length;
}
function da(n, e, t) {
  var i = this && this.__awaiter || function(v, T, k, w) {
    function g(b) {
      return b instanceof k ? b : new k(function(O) {
        O(b);
      });
    }
    return new (k || (k = Promise))(function(b, O) {
      function P(F) {
        try {
          j(w.next(F));
        } catch (L) {
          O(L);
        }
      }
      function U(F) {
        try {
          j(w.throw(F));
        } catch (L) {
          O(L);
        }
      }
      function j(F) {
        F.done ? b(F.value) : g(F.value).then(P, U);
      }
      j((w = w.apply(v, T || [])).next());
    });
  };
  let { upload_id: l } = e, { root: o } = e, { files: a } = e, { stream_handler: s } = e, r, f = !1, _, d, c = a.map((v) => Object.assign(Object.assign({}, v), { progress: 0 }));
  const u = fa();
  function h(v, T) {
    t(0, c = c.map((k) => (k.orig_name === v && (k.progress += T), k)));
  }
  return sa(() => i(void 0, void 0, void 0, function* () {
    if (r = yield s(new URL(`${o}/gradio_api/upload_progress?upload_id=${l}`)), r == null)
      throw new Error("Event source is not defined");
    r.onmessage = function(v) {
      return i(this, void 0, void 0, function* () {
        const T = JSON.parse(v.data);
        f || t(1, f = !0), T.msg === "done" ? (r == null || r.close(), u("done")) : (t(7, _ = T), h(T.orig_name, T.chunk_size));
      });
    };
  })), ua(() => {
    (r != null || r != null) && r.close();
  }), n.$$set = (v) => {
    "upload_id" in v && t(3, l = v.upload_id), "root" in v && t(4, o = v.root), "files" in v && t(5, a = v.files), "stream_handler" in v && t(6, s = v.stream_handler);
  }, n.$$.update = () => {
    n.$$.dirty & /*files_with_progress*/
    1 && _a(c), n.$$.dirty & /*current_file_upload, files_with_progress*/
    129 && t(2, d = _ || c[0]);
  }, [
    c,
    f,
    d,
    l,
    o,
    a,
    s,
    _
  ];
}
class ma extends oa {
  constructor(e) {
    super(), aa(this, e, da, ca, ra, {
      upload_id: 3,
      root: 4,
      files: 5,
      stream_handler: 6
    });
  }
}
const {
  SvelteComponent: ha,
  append_hydration: cl,
  attr: De,
  binding_callbacks: ga,
  bubble: zt,
  check_outros: po,
  children: wo,
  claim_component: ba,
  claim_element: Mi,
  claim_space: pa,
  create_component: wa,
  create_slot: vo,
  destroy_component: va,
  detach: gn,
  element: Pi,
  empty: si,
  get_all_dirty_from_scope: ko,
  get_slot_changes: yo,
  group_outros: Eo,
  init: ka,
  insert_hydration: di,
  listen: He,
  mount_component: ya,
  prevent_default: qt,
  run_all: Ea,
  safe_not_equal: Ta,
  set_style: To,
  space: Aa,
  stop_propagation: Bt,
  toggle_class: we,
  transition_in: Rt,
  transition_out: en,
  update_slot_base: Ao
} = window.__gradio__svelte__internal, { createEventDispatcher: Sa, tick: Da } = window.__gradio__svelte__internal;
function La(n) {
  let e, t, i, l, o, a, s, r, f, _, d;
  const c = (
    /*#slots*/
    n[27].default
  ), u = vo(
    c,
    n,
    /*$$scope*/
    n[26],
    null
  );
  return {
    c() {
      e = Pi("button"), u && u.c(), t = Aa(), i = Pi("input"), this.h();
    },
    l(h) {
      e = Mi(h, "BUTTON", { tabindex: !0, class: !0 });
      var v = wo(e);
      u && u.l(v), t = pa(v), i = Mi(v, "INPUT", {
        "aria-label": !0,
        "data-testid": !0,
        type: !0,
        accept: !0,
        webkitdirectory: !0,
        mozdirectory: !0,
        class: !0
      }), v.forEach(gn), this.h();
    },
    h() {
      De(i, "aria-label", "file upload"), De(i, "data-testid", "file-upload"), De(i, "type", "file"), De(i, "accept", l = /*accept_file_types*/
      n[16] || void 0), i.multiple = o = /*file_count*/
      n[6] === "multiple" || void 0, De(i, "webkitdirectory", a = /*file_count*/
      n[6] === "directory" || void 0), De(i, "mozdirectory", s = /*file_count*/
      n[6] === "directory" || void 0), De(i, "class", "svelte-ks67v6"), De(e, "tabindex", r = /*hidden*/
      n[9] ? -1 : 0), De(e, "class", "svelte-ks67v6"), we(
        e,
        "hidden",
        /*hidden*/
        n[9]
      ), we(
        e,
        "center",
        /*center*/
        n[4]
      ), we(
        e,
        "boundedheight",
        /*boundedheight*/
        n[3]
      ), we(
        e,
        "flex",
        /*flex*/
        n[5]
      ), we(
        e,
        "disable_click",
        /*disable_click*/
        n[7]
      ), To(e, "height", "100%");
    },
    m(h, v) {
      di(h, e, v), u && u.m(e, null), cl(e, t), cl(e, i), n[35](i), f = !0, _ || (d = [
        He(
          i,
          "change",
          /*load_files_from_upload*/
          n[18]
        ),
        He(e, "drag", Bt(qt(
          /*drag_handler*/
          n[28]
        ))),
        He(e, "dragstart", Bt(qt(
          /*dragstart_handler*/
          n[29]
        ))),
        He(e, "dragend", Bt(qt(
          /*dragend_handler*/
          n[30]
        ))),
        He(e, "dragover", Bt(qt(
          /*dragover_handler*/
          n[31]
        ))),
        He(e, "dragenter", Bt(qt(
          /*dragenter_handler*/
          n[32]
        ))),
        He(e, "dragleave", Bt(qt(
          /*dragleave_handler*/
          n[33]
        ))),
        He(e, "drop", Bt(qt(
          /*drop_handler*/
          n[34]
        ))),
        He(
          e,
          "click",
          /*open_file_upload*/
          n[13]
        ),
        He(
          e,
          "drop",
          /*loadFilesFromDrop*/
          n[19]
        ),
        He(
          e,
          "dragenter",
          /*updateDragging*/
          n[17]
        ),
        He(
          e,
          "dragleave",
          /*updateDragging*/
          n[17]
        )
      ], _ = !0);
    },
    p(h, v) {
      u && u.p && (!f || v[0] & /*$$scope*/
      67108864) && Ao(
        u,
        c,
        h,
        /*$$scope*/
        h[26],
        f ? yo(
          c,
          /*$$scope*/
          h[26],
          v,
          null
        ) : ko(
          /*$$scope*/
          h[26]
        ),
        null
      ), (!f || v[0] & /*accept_file_types*/
      65536 && l !== (l = /*accept_file_types*/
      h[16] || void 0)) && De(i, "accept", l), (!f || v[0] & /*file_count*/
      64 && o !== (o = /*file_count*/
      h[6] === "multiple" || void 0)) && (i.multiple = o), (!f || v[0] & /*file_count*/
      64 && a !== (a = /*file_count*/
      h[6] === "directory" || void 0)) && De(i, "webkitdirectory", a), (!f || v[0] & /*file_count*/
      64 && s !== (s = /*file_count*/
      h[6] === "directory" || void 0)) && De(i, "mozdirectory", s), (!f || v[0] & /*hidden*/
      512 && r !== (r = /*hidden*/
      h[9] ? -1 : 0)) && De(e, "tabindex", r), (!f || v[0] & /*hidden*/
      512) && we(
        e,
        "hidden",
        /*hidden*/
        h[9]
      ), (!f || v[0] & /*center*/
      16) && we(
        e,
        "center",
        /*center*/
        h[4]
      ), (!f || v[0] & /*boundedheight*/
      8) && we(
        e,
        "boundedheight",
        /*boundedheight*/
        h[3]
      ), (!f || v[0] & /*flex*/
      32) && we(
        e,
        "flex",
        /*flex*/
        h[5]
      ), (!f || v[0] & /*disable_click*/
      128) && we(
        e,
        "disable_click",
        /*disable_click*/
        h[7]
      );
    },
    i(h) {
      f || (Rt(u, h), f = !0);
    },
    o(h) {
      en(u, h), f = !1;
    },
    d(h) {
      h && gn(e), u && u.d(h), n[35](null), _ = !1, Ea(d);
    }
  };
}
function Ca(n) {
  let e, t, i = !/*hidden*/
  n[9] && _l(n);
  return {
    c() {
      i && i.c(), e = si();
    },
    l(l) {
      i && i.l(l), e = si();
    },
    m(l, o) {
      i && i.m(l, o), di(l, e, o), t = !0;
    },
    p(l, o) {
      /*hidden*/
      l[9] ? i && (Eo(), en(i, 1, 1, () => {
        i = null;
      }), po()) : i ? (i.p(l, o), o[0] & /*hidden*/
      512 && Rt(i, 1)) : (i = _l(l), i.c(), Rt(i, 1), i.m(e.parentNode, e));
    },
    i(l) {
      t || (Rt(i), t = !0);
    },
    o(l) {
      en(i), t = !1;
    },
    d(l) {
      l && gn(e), i && i.d(l);
    }
  };
}
function Ia(n) {
  let e, t, i, l, o;
  const a = (
    /*#slots*/
    n[27].default
  ), s = vo(
    a,
    n,
    /*$$scope*/
    n[26],
    null
  );
  return {
    c() {
      e = Pi("button"), s && s.c(), this.h();
    },
    l(r) {
      e = Mi(r, "BUTTON", { tabindex: !0, class: !0 });
      var f = wo(e);
      s && s.l(f), f.forEach(gn), this.h();
    },
    h() {
      De(e, "tabindex", t = /*hidden*/
      n[9] ? -1 : 0), De(e, "class", "svelte-ks67v6"), we(
        e,
        "hidden",
        /*hidden*/
        n[9]
      ), we(
        e,
        "center",
        /*center*/
        n[4]
      ), we(
        e,
        "boundedheight",
        /*boundedheight*/
        n[3]
      ), we(
        e,
        "flex",
        /*flex*/
        n[5]
      ), To(e, "height", "100%");
    },
    m(r, f) {
      di(r, e, f), s && s.m(e, null), i = !0, l || (o = He(
        e,
        "click",
        /*paste_clipboard*/
        n[12]
      ), l = !0);
    },
    p(r, f) {
      s && s.p && (!i || f[0] & /*$$scope*/
      67108864) && Ao(
        s,
        a,
        r,
        /*$$scope*/
        r[26],
        i ? yo(
          a,
          /*$$scope*/
          r[26],
          f,
          null
        ) : ko(
          /*$$scope*/
          r[26]
        ),
        null
      ), (!i || f[0] & /*hidden*/
      512 && t !== (t = /*hidden*/
      r[9] ? -1 : 0)) && De(e, "tabindex", t), (!i || f[0] & /*hidden*/
      512) && we(
        e,
        "hidden",
        /*hidden*/
        r[9]
      ), (!i || f[0] & /*center*/
      16) && we(
        e,
        "center",
        /*center*/
        r[4]
      ), (!i || f[0] & /*boundedheight*/
      8) && we(
        e,
        "boundedheight",
        /*boundedheight*/
        r[3]
      ), (!i || f[0] & /*flex*/
      32) && we(
        e,
        "flex",
        /*flex*/
        r[5]
      );
    },
    i(r) {
      i || (Rt(s, r), i = !0);
    },
    o(r) {
      en(s, r), i = !1;
    },
    d(r) {
      r && gn(e), s && s.d(r), l = !1, o();
    }
  };
}
function _l(n) {
  let e, t;
  return e = new ma({
    props: {
      root: (
        /*root*/
        n[8]
      ),
      upload_id: (
        /*upload_id*/
        n[14]
      ),
      files: (
        /*file_data*/
        n[15]
      ),
      stream_handler: (
        /*stream_handler*/
        n[11]
      )
    }
  }), {
    c() {
      wa(e.$$.fragment);
    },
    l(i) {
      ba(e.$$.fragment, i);
    },
    m(i, l) {
      ya(e, i, l), t = !0;
    },
    p(i, l) {
      const o = {};
      l[0] & /*root*/
      256 && (o.root = /*root*/
      i[8]), l[0] & /*upload_id*/
      16384 && (o.upload_id = /*upload_id*/
      i[14]), l[0] & /*file_data*/
      32768 && (o.files = /*file_data*/
      i[15]), l[0] & /*stream_handler*/
      2048 && (o.stream_handler = /*stream_handler*/
      i[11]), e.$set(o);
    },
    i(i) {
      t || (Rt(e.$$.fragment, i), t = !0);
    },
    o(i) {
      en(e.$$.fragment, i), t = !1;
    },
    d(i) {
      va(e, i);
    }
  };
}
function Na(n) {
  let e, t, i, l;
  const o = [Ia, Ca, La], a = [];
  function s(r, f) {
    return (
      /*filetype*/
      r[0] === "clipboard" ? 0 : (
        /*uploading*/
        r[1] && /*show_progress*/
        r[10] ? 1 : 2
      )
    );
  }
  return e = s(n), t = a[e] = o[e](n), {
    c() {
      t.c(), i = si();
    },
    l(r) {
      t.l(r), i = si();
    },
    m(r, f) {
      a[e].m(r, f), di(r, i, f), l = !0;
    },
    p(r, f) {
      let _ = e;
      e = s(r), e === _ ? a[e].p(r, f) : (Eo(), en(a[_], 1, 1, () => {
        a[_] = null;
      }), po(), t = a[e], t ? t.p(r, f) : (t = a[e] = o[e](r), t.c()), Rt(t, 1), t.m(i.parentNode, i));
    },
    i(r) {
      l || (Rt(t), l = !0);
    },
    o(r) {
      en(t), l = !1;
    },
    d(r) {
      r && gn(i), a[e].d(r);
    }
  };
}
function Oa(n, e, t) {
  if (!n || n === "*" || n === "file/*" || Array.isArray(n) && n.some((l) => l === "*" || l === "file/*"))
    return !0;
  let i;
  if (typeof n == "string")
    i = n.split(",").map((l) => l.trim());
  else if (Array.isArray(n))
    i = n;
  else
    return !1;
  return i.includes(e) || i.some((l) => {
    const [o] = l.split("/").map((a) => a.trim());
    return l.endsWith("/*") && t.startsWith(o + "/");
  });
}
function Ra(n, e, t) {
  let i, { $$slots: l = {}, $$scope: o } = e;
  var a = this && this.__awaiter || function(y, M, H, q) {
    function x(ce) {
      return ce instanceof H ? ce : new H(function(_e) {
        _e(ce);
      });
    }
    return new (H || (H = Promise))(function(ce, _e) {
      function me(Re) {
        try {
          fe(q.next(Re));
        } catch (vt) {
          _e(vt);
        }
      }
      function Ae(Re) {
        try {
          fe(q.throw(Re));
        } catch (vt) {
          _e(vt);
        }
      }
      function fe(Re) {
        Re.done ? ce(Re.value) : x(Re.value).then(me, Ae);
      }
      fe((q = q.apply(y, M || [])).next());
    });
  };
  let { filetype: s = null } = e, { dragging: r = !1 } = e, { boundedheight: f = !0 } = e, { center: _ = !0 } = e, { flex: d = !0 } = e, { file_count: c = "single" } = e, { disable_click: u = !1 } = e, { root: h } = e, { hidden: v = !1 } = e, { format: T = "file" } = e, { uploading: k = !1 } = e, { hidden_upload: w = null } = e, { show_progress: g = !0 } = e, { max_file_size: b = null } = e, { upload: O } = e, { stream_handler: P } = e, U, j, F, L = null;
  const J = () => {
    if (typeof navigator < "u") {
      const y = navigator.userAgent.toLowerCase();
      return y.indexOf("iphone") > -1 || y.indexOf("ipad") > -1;
    }
    return !1;
  }, Y = Sa(), ne = ["image", "video", "audio", "text", "file"], B = (y) => i && y.startsWith(".") ? (L = !0, y) : i && y.includes("file/*") ? "*" : y.startsWith(".") || y.endsWith("/*") ? y : ne.includes(y) ? y + "/*" : "." + y;
  function ie() {
    t(20, r = !r);
  }
  function se() {
    navigator.clipboard.read().then((y) => a(this, void 0, void 0, function* () {
      for (let M = 0; M < y.length; M++) {
        const H = y[M].types.find((q) => q.startsWith("image/"));
        if (H) {
          y[M].getType(H).then((q) => a(this, void 0, void 0, function* () {
            const x = new File([q], `clipboard.${H.replace("image/", "")}`);
            yield be([x]);
          }));
          break;
        }
      }
    }));
  }
  function Oe() {
    u || w && (t(2, w.value = "", w), w.click());
  }
  function de(y) {
    return a(this, void 0, void 0, function* () {
      yield Da(), t(14, U = Math.random().toString(36).substring(2, 15)), t(1, k = !0);
      try {
        const M = yield O(y, h, U, b ?? 1 / 0);
        return Y("load", c === "single" ? M == null ? void 0 : M[0] : M), t(1, k = !1), M || [];
      } catch (M) {
        return Y("error", M.message), t(1, k = !1), [];
      }
    });
  }
  function be(y) {
    return a(this, void 0, void 0, function* () {
      if (!y.length)
        return;
      let M = y.map((H) => new File([H], H instanceof File ? H.name : "file", { type: H.type }));
      return i && L && (M = M.filter((H) => Le(H) ? !0 : (Y("error", `Invalid file type: ${H.name}. Only ${s} allowed.`), !1)), M.length === 0) ? [] : (t(15, j = yield ia(M)), yield de(j));
    });
  }
  function Le(y) {
    return s ? (Array.isArray(s) ? s : [s]).some((H) => {
      const q = B(H);
      if (q.startsWith("."))
        return y.name.toLowerCase().endsWith(q.toLowerCase());
      if (q === "*")
        return !0;
      if (q.endsWith("/*")) {
        const [x] = q.split("/");
        return y.type.startsWith(x + "/");
      }
      return y.type === q;
    }) : !0;
  }
  function K(y) {
    return a(this, void 0, void 0, function* () {
      const M = y.target;
      if (M.files)
        if (T != "blob")
          yield be(Array.from(M.files));
        else {
          if (c === "single") {
            Y("load", M.files[0]);
            return;
          }
          Y("load", M.files);
        }
    });
  }
  function ve(y) {
    return a(this, void 0, void 0, function* () {
      var M;
      if (t(20, r = !1), !(!((M = y.dataTransfer) === null || M === void 0) && M.files)) return;
      const H = Array.from(y.dataTransfer.files).filter((q) => {
        const x = "." + q.name.split(".").pop();
        return x && Oa(F, x, q.type) || (x && Array.isArray(s) ? s.includes(x) : x === s) ? !0 : (Y("error", `Invalid file type only ${s} allowed.`), !1);
      });
      if (T != "blob")
        yield be(H);
      else {
        if (c === "single") {
          Y("load", H[0]);
          return;
        }
        Y("load", H);
      }
    });
  }
  function X(y) {
    zt.call(this, n, y);
  }
  function le(y) {
    zt.call(this, n, y);
  }
  function S(y) {
    zt.call(this, n, y);
  }
  function Te(y) {
    zt.call(this, n, y);
  }
  function pe(y) {
    zt.call(this, n, y);
  }
  function D(y) {
    zt.call(this, n, y);
  }
  function Z(y) {
    zt.call(this, n, y);
  }
  function ee(y) {
    ga[y ? "unshift" : "push"](() => {
      w = y, t(2, w);
    });
  }
  return n.$$set = (y) => {
    "filetype" in y && t(0, s = y.filetype), "dragging" in y && t(20, r = y.dragging), "boundedheight" in y && t(3, f = y.boundedheight), "center" in y && t(4, _ = y.center), "flex" in y && t(5, d = y.flex), "file_count" in y && t(6, c = y.file_count), "disable_click" in y && t(7, u = y.disable_click), "root" in y && t(8, h = y.root), "hidden" in y && t(9, v = y.hidden), "format" in y && t(21, T = y.format), "uploading" in y && t(1, k = y.uploading), "hidden_upload" in y && t(2, w = y.hidden_upload), "show_progress" in y && t(10, g = y.show_progress), "max_file_size" in y && t(22, b = y.max_file_size), "upload" in y && t(23, O = y.upload), "stream_handler" in y && t(11, P = y.stream_handler), "$$scope" in y && t(26, o = y.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*filetype, ios*/
    33554433 && (s == null ? t(16, F = null) : typeof s == "string" ? t(16, F = B(s)) : i && s.includes("file/*") ? t(16, F = "*") : (t(0, s = s.map(B)), t(16, F = s.join(", "))));
  }, t(25, i = J()), [
    s,
    k,
    w,
    f,
    _,
    d,
    c,
    u,
    h,
    v,
    g,
    P,
    se,
    Oe,
    U,
    j,
    F,
    ie,
    K,
    ve,
    r,
    T,
    b,
    O,
    be,
    i,
    o,
    l,
    X,
    le,
    S,
    Te,
    pe,
    D,
    Z,
    ee
  ];
}
class Ma extends ha {
  constructor(e) {
    super(), ka(
      this,
      e,
      Ra,
      Na,
      Ta,
      {
        filetype: 0,
        dragging: 20,
        boundedheight: 3,
        center: 4,
        flex: 5,
        file_count: 6,
        disable_click: 7,
        root: 8,
        hidden: 9,
        format: 21,
        uploading: 1,
        hidden_upload: 2,
        show_progress: 10,
        max_file_size: 22,
        upload: 23,
        stream_handler: 11,
        paste_clipboard: 12,
        open_file_upload: 13,
        load_files: 24
      },
      null,
      [-1, -1]
    );
  }
  get paste_clipboard() {
    return this.$$.ctx[12];
  }
  get open_file_upload() {
    return this.$$.ctx[13];
  }
  get load_files() {
    return this.$$.ctx[24];
  }
}
const {
  SvelteComponent: Pa,
  assign: Fa,
  children: Ua,
  claim_element: za,
  create_slot: qa,
  detach: dl,
  element: Ba,
  get_all_dirty_from_scope: Ha,
  get_slot_changes: Wa,
  get_spread_update: Va,
  init: Ga,
  insert_hydration: ja,
  safe_not_equal: Ya,
  set_dynamic_element_data: ml,
  set_style: ye,
  toggle_class: Ge,
  transition_in: So,
  transition_out: Do,
  update_slot_base: Xa
} = window.__gradio__svelte__internal;
function Za(n) {
  let e, t, i;
  const l = (
    /*#slots*/
    n[22].default
  ), o = qa(
    l,
    n,
    /*$$scope*/
    n[21],
    null
  );
  let a = [
    { "data-testid": (
      /*test_id*/
      n[10]
    ) },
    { id: (
      /*elem_id*/
      n[5]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      n[6].join(" ") + " svelte-1ezsyiy"
    }
  ], s = {};
  for (let r = 0; r < a.length; r += 1)
    s = Fa(s, a[r]);
  return {
    c() {
      e = Ba(
        /*tag*/
        n[18]
      ), o && o.c(), this.h();
    },
    l(r) {
      e = za(
        r,
        /*tag*/
        (n[18] || "null").toUpperCase(),
        {
          "data-testid": !0,
          id: !0,
          class: !0
        }
      );
      var f = Ua(e);
      o && o.l(f), f.forEach(dl), this.h();
    },
    h() {
      ml(
        /*tag*/
        n[18]
      )(e, s), Ge(
        e,
        "hidden",
        /*visible*/
        n[13] === !1
      ), Ge(
        e,
        "padded",
        /*padding*/
        n[9]
      ), Ge(
        e,
        "flex",
        /*flex*/
        n[0]
      ), Ge(
        e,
        "border_focus",
        /*border_mode*/
        n[8] === "focus"
      ), Ge(
        e,
        "border_contrast",
        /*border_mode*/
        n[8] === "contrast"
      ), Ge(e, "hide-container", !/*explicit_call*/
      n[11] && !/*container*/
      n[12]), ye(
        e,
        "height",
        /*get_dimension*/
        n[19](
          /*height*/
          n[1]
        )
      ), ye(
        e,
        "min-height",
        /*get_dimension*/
        n[19](
          /*min_height*/
          n[2]
        )
      ), ye(
        e,
        "max-height",
        /*get_dimension*/
        n[19](
          /*max_height*/
          n[3]
        )
      ), ye(e, "width", typeof /*width*/
      n[4] == "number" ? `calc(min(${/*width*/
      n[4]}px, 100%))` : (
        /*get_dimension*/
        n[19](
          /*width*/
          n[4]
        )
      )), ye(
        e,
        "border-style",
        /*variant*/
        n[7]
      ), ye(
        e,
        "overflow",
        /*allow_overflow*/
        n[14] ? (
          /*overflow_behavior*/
          n[15]
        ) : "hidden"
      ), ye(
        e,
        "flex-grow",
        /*scale*/
        n[16]
      ), ye(e, "min-width", `calc(min(${/*min_width*/
      n[17]}px, 100%))`), ye(e, "border-width", "var(--block-border-width)");
    },
    m(r, f) {
      ja(r, e, f), o && o.m(e, null), i = !0;
    },
    p(r, f) {
      o && o.p && (!i || f & /*$$scope*/
      2097152) && Xa(
        o,
        l,
        r,
        /*$$scope*/
        r[21],
        i ? Wa(
          l,
          /*$$scope*/
          r[21],
          f,
          null
        ) : Ha(
          /*$$scope*/
          r[21]
        ),
        null
      ), ml(
        /*tag*/
        r[18]
      )(e, s = Va(a, [
        (!i || f & /*test_id*/
        1024) && { "data-testid": (
          /*test_id*/
          r[10]
        ) },
        (!i || f & /*elem_id*/
        32) && { id: (
          /*elem_id*/
          r[5]
        ) },
        (!i || f & /*elem_classes*/
        64 && t !== (t = "block " + /*elem_classes*/
        r[6].join(" ") + " svelte-1ezsyiy")) && { class: t }
      ])), Ge(
        e,
        "hidden",
        /*visible*/
        r[13] === !1
      ), Ge(
        e,
        "padded",
        /*padding*/
        r[9]
      ), Ge(
        e,
        "flex",
        /*flex*/
        r[0]
      ), Ge(
        e,
        "border_focus",
        /*border_mode*/
        r[8] === "focus"
      ), Ge(
        e,
        "border_contrast",
        /*border_mode*/
        r[8] === "contrast"
      ), Ge(e, "hide-container", !/*explicit_call*/
      r[11] && !/*container*/
      r[12]), f & /*height*/
      2 && ye(
        e,
        "height",
        /*get_dimension*/
        r[19](
          /*height*/
          r[1]
        )
      ), f & /*min_height*/
      4 && ye(
        e,
        "min-height",
        /*get_dimension*/
        r[19](
          /*min_height*/
          r[2]
        )
      ), f & /*max_height*/
      8 && ye(
        e,
        "max-height",
        /*get_dimension*/
        r[19](
          /*max_height*/
          r[3]
        )
      ), f & /*width*/
      16 && ye(e, "width", typeof /*width*/
      r[4] == "number" ? `calc(min(${/*width*/
      r[4]}px, 100%))` : (
        /*get_dimension*/
        r[19](
          /*width*/
          r[4]
        )
      )), f & /*variant*/
      128 && ye(
        e,
        "border-style",
        /*variant*/
        r[7]
      ), f & /*allow_overflow, overflow_behavior*/
      49152 && ye(
        e,
        "overflow",
        /*allow_overflow*/
        r[14] ? (
          /*overflow_behavior*/
          r[15]
        ) : "hidden"
      ), f & /*scale*/
      65536 && ye(
        e,
        "flex-grow",
        /*scale*/
        r[16]
      ), f & /*min_width*/
      131072 && ye(e, "min-width", `calc(min(${/*min_width*/
      r[17]}px, 100%))`);
    },
    i(r) {
      i || (So(o, r), i = !0);
    },
    o(r) {
      Do(o, r), i = !1;
    },
    d(r) {
      r && dl(e), o && o.d(r);
    }
  };
}
function Ka(n) {
  let e, t = (
    /*tag*/
    n[18] && Za(n)
  );
  return {
    c() {
      t && t.c();
    },
    l(i) {
      t && t.l(i);
    },
    m(i, l) {
      t && t.m(i, l), e = !0;
    },
    p(i, [l]) {
      /*tag*/
      i[18] && t.p(i, l);
    },
    i(i) {
      e || (So(t, i), e = !0);
    },
    o(i) {
      Do(t, i), e = !1;
    },
    d(i) {
      t && t.d(i);
    }
  };
}
function Ja(n, e, t) {
  let { $$slots: i = {}, $$scope: l } = e, { height: o = void 0 } = e, { min_height: a = void 0 } = e, { max_height: s = void 0 } = e, { width: r = void 0 } = e, { elem_id: f = "" } = e, { elem_classes: _ = [] } = e, { variant: d = "solid" } = e, { border_mode: c = "base" } = e, { padding: u = !0 } = e, { type: h = "normal" } = e, { test_id: v = void 0 } = e, { explicit_call: T = !1 } = e, { container: k = !0 } = e, { visible: w = !0 } = e, { allow_overflow: g = !0 } = e, { overflow_behavior: b = "auto" } = e, { scale: O = null } = e, { min_width: P = 0 } = e, { flex: U = !1 } = e;
  w || (U = !1);
  let j = h === "fieldset" ? "fieldset" : "div";
  const F = (L) => {
    if (L !== void 0) {
      if (typeof L == "number")
        return L + "px";
      if (typeof L == "string")
        return L;
    }
  };
  return n.$$set = (L) => {
    "height" in L && t(1, o = L.height), "min_height" in L && t(2, a = L.min_height), "max_height" in L && t(3, s = L.max_height), "width" in L && t(4, r = L.width), "elem_id" in L && t(5, f = L.elem_id), "elem_classes" in L && t(6, _ = L.elem_classes), "variant" in L && t(7, d = L.variant), "border_mode" in L && t(8, c = L.border_mode), "padding" in L && t(9, u = L.padding), "type" in L && t(20, h = L.type), "test_id" in L && t(10, v = L.test_id), "explicit_call" in L && t(11, T = L.explicit_call), "container" in L && t(12, k = L.container), "visible" in L && t(13, w = L.visible), "allow_overflow" in L && t(14, g = L.allow_overflow), "overflow_behavior" in L && t(15, b = L.overflow_behavior), "scale" in L && t(16, O = L.scale), "min_width" in L && t(17, P = L.min_width), "flex" in L && t(0, U = L.flex), "$$scope" in L && t(21, l = L.$$scope);
  }, [
    U,
    o,
    a,
    s,
    r,
    f,
    _,
    d,
    c,
    u,
    v,
    T,
    k,
    w,
    g,
    b,
    O,
    P,
    j,
    F,
    h,
    l,
    i
  ];
}
class Qa extends Pa {
  constructor(e) {
    super(), Ga(this, e, Ja, Ka, Ya, {
      height: 1,
      min_height: 2,
      max_height: 3,
      width: 4,
      elem_id: 5,
      elem_classes: 6,
      variant: 7,
      border_mode: 8,
      padding: 9,
      type: 20,
      test_id: 10,
      explicit_call: 11,
      container: 12,
      visible: 13,
      allow_overflow: 14,
      overflow_behavior: 15,
      scale: 16,
      min_width: 17,
      flex: 0
    });
  }
}
const {
  SvelteComponent: xa,
  append_hydration: Fi,
  attr: kt,
  bubble: $a,
  check_outros: er,
  children: Ui,
  claim_component: tr,
  claim_element: zi,
  claim_space: nr,
  claim_text: ir,
  construct_svelte_component: hl,
  create_component: gl,
  destroy_component: bl,
  detach: Fn,
  element: qi,
  group_outros: lr,
  init: or,
  insert_hydration: Lo,
  listen: ar,
  mount_component: pl,
  safe_not_equal: rr,
  set_data: sr,
  set_style: Zn,
  space: fr,
  text: ur,
  toggle_class: Pe,
  transition_in: wl,
  transition_out: vl
} = window.__gradio__svelte__internal;
function kl(n) {
  let e, t;
  return {
    c() {
      e = qi("span"), t = ur(
        /*label*/
        n[1]
      ), this.h();
    },
    l(i) {
      e = zi(i, "SPAN", { class: !0 });
      var l = Ui(e);
      t = ir(
        l,
        /*label*/
        n[1]
      ), l.forEach(Fn), this.h();
    },
    h() {
      kt(e, "class", "svelte-vk34kx");
    },
    m(i, l) {
      Lo(i, e, l), Fi(e, t);
    },
    p(i, l) {
      l & /*label*/
      2 && sr(
        t,
        /*label*/
        i[1]
      );
    },
    d(i) {
      i && Fn(e);
    }
  };
}
function cr(n) {
  let e, t, i, l, o, a, s, r = (
    /*show_label*/
    n[2] && kl(n)
  );
  var f = (
    /*Icon*/
    n[0]
  );
  function _(d, c) {
    return {};
  }
  return f && (l = hl(f, _())), {
    c() {
      e = qi("button"), r && r.c(), t = fr(), i = qi("div"), l && gl(l.$$.fragment), this.h();
    },
    l(d) {
      e = zi(d, "BUTTON", {
        "aria-label": !0,
        "aria-haspopup": !0,
        title: !0,
        class: !0
      });
      var c = Ui(e);
      r && r.l(c), t = nr(c), i = zi(c, "DIV", { class: !0 });
      var u = Ui(i);
      l && tr(l.$$.fragment, u), u.forEach(Fn), c.forEach(Fn), this.h();
    },
    h() {
      kt(i, "class", "svelte-vk34kx"), Pe(
        i,
        "small",
        /*size*/
        n[4] === "small"
      ), Pe(
        i,
        "large",
        /*size*/
        n[4] === "large"
      ), Pe(
        i,
        "medium",
        /*size*/
        n[4] === "medium"
      ), e.disabled = /*disabled*/
      n[7], kt(
        e,
        "aria-label",
        /*label*/
        n[1]
      ), kt(
        e,
        "aria-haspopup",
        /*hasPopup*/
        n[8]
      ), kt(
        e,
        "title",
        /*label*/
        n[1]
      ), kt(e, "class", "svelte-vk34kx"), Pe(
        e,
        "pending",
        /*pending*/
        n[3]
      ), Pe(
        e,
        "padded",
        /*padded*/
        n[5]
      ), Pe(
        e,
        "highlight",
        /*highlight*/
        n[6]
      ), Pe(
        e,
        "transparent",
        /*transparent*/
        n[9]
      ), Zn(e, "color", !/*disabled*/
      n[7] && /*_color*/
      n[11] ? (
        /*_color*/
        n[11]
      ) : "var(--block-label-text-color)"), Zn(e, "--bg-color", /*disabled*/
      n[7] ? "auto" : (
        /*background*/
        n[10]
      ));
    },
    m(d, c) {
      Lo(d, e, c), r && r.m(e, null), Fi(e, t), Fi(e, i), l && pl(l, i, null), o = !0, a || (s = ar(
        e,
        "click",
        /*click_handler*/
        n[13]
      ), a = !0);
    },
    p(d, [c]) {
      if (/*show_label*/
      d[2] ? r ? r.p(d, c) : (r = kl(d), r.c(), r.m(e, t)) : r && (r.d(1), r = null), c & /*Icon*/
      1 && f !== (f = /*Icon*/
      d[0])) {
        if (l) {
          lr();
          const u = l;
          vl(u.$$.fragment, 1, 0, () => {
            bl(u, 1);
          }), er();
        }
        f ? (l = hl(f, _()), gl(l.$$.fragment), wl(l.$$.fragment, 1), pl(l, i, null)) : l = null;
      }
      (!o || c & /*size*/
      16) && Pe(
        i,
        "small",
        /*size*/
        d[4] === "small"
      ), (!o || c & /*size*/
      16) && Pe(
        i,
        "large",
        /*size*/
        d[4] === "large"
      ), (!o || c & /*size*/
      16) && Pe(
        i,
        "medium",
        /*size*/
        d[4] === "medium"
      ), (!o || c & /*disabled*/
      128) && (e.disabled = /*disabled*/
      d[7]), (!o || c & /*label*/
      2) && kt(
        e,
        "aria-label",
        /*label*/
        d[1]
      ), (!o || c & /*hasPopup*/
      256) && kt(
        e,
        "aria-haspopup",
        /*hasPopup*/
        d[8]
      ), (!o || c & /*label*/
      2) && kt(
        e,
        "title",
        /*label*/
        d[1]
      ), (!o || c & /*pending*/
      8) && Pe(
        e,
        "pending",
        /*pending*/
        d[3]
      ), (!o || c & /*padded*/
      32) && Pe(
        e,
        "padded",
        /*padded*/
        d[5]
      ), (!o || c & /*highlight*/
      64) && Pe(
        e,
        "highlight",
        /*highlight*/
        d[6]
      ), (!o || c & /*transparent*/
      512) && Pe(
        e,
        "transparent",
        /*transparent*/
        d[9]
      ), c & /*disabled, _color*/
      2176 && Zn(e, "color", !/*disabled*/
      d[7] && /*_color*/
      d[11] ? (
        /*_color*/
        d[11]
      ) : "var(--block-label-text-color)"), c & /*disabled, background*/
      1152 && Zn(e, "--bg-color", /*disabled*/
      d[7] ? "auto" : (
        /*background*/
        d[10]
      ));
    },
    i(d) {
      o || (l && wl(l.$$.fragment, d), o = !0);
    },
    o(d) {
      l && vl(l.$$.fragment, d), o = !1;
    },
    d(d) {
      d && Fn(e), r && r.d(), l && bl(l), a = !1, s();
    }
  };
}
function _r(n, e, t) {
  let i, { Icon: l } = e, { label: o = "" } = e, { show_label: a = !1 } = e, { pending: s = !1 } = e, { size: r = "small" } = e, { padded: f = !0 } = e, { highlight: _ = !1 } = e, { disabled: d = !1 } = e, { hasPopup: c = !1 } = e, { color: u = "var(--block-label-text-color)" } = e, { transparent: h = !1 } = e, { background: v = "var(--block-background-fill)" } = e;
  function T(k) {
    $a.call(this, n, k);
  }
  return n.$$set = (k) => {
    "Icon" in k && t(0, l = k.Icon), "label" in k && t(1, o = k.label), "show_label" in k && t(2, a = k.show_label), "pending" in k && t(3, s = k.pending), "size" in k && t(4, r = k.size), "padded" in k && t(5, f = k.padded), "highlight" in k && t(6, _ = k.highlight), "disabled" in k && t(7, d = k.disabled), "hasPopup" in k && t(8, c = k.hasPopup), "color" in k && t(12, u = k.color), "transparent" in k && t(9, h = k.transparent), "background" in k && t(10, v = k.background);
  }, n.$$.update = () => {
    n.$$.dirty & /*highlight, color*/
    4160 && t(11, i = _ ? "var(--color-accent)" : u);
  }, [
    l,
    o,
    a,
    s,
    r,
    f,
    _,
    d,
    c,
    h,
    v,
    i,
    u,
    T
  ];
}
class dr extends xa {
  constructor(e) {
    super(), or(this, e, _r, cr, rr, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 12,
      transparent: 9,
      background: 10
    });
  }
}
const {
  SvelteComponent: mr,
  append_hydration: vi,
  attr: et,
  children: Kn,
  claim_svg_element: Jn,
  detach: Dn,
  init: hr,
  insert_hydration: gr,
  noop: ki,
  safe_not_equal: br,
  set_style: ct,
  svg_element: Qn
} = window.__gradio__svelte__internal;
function pr(n) {
  let e, t, i, l;
  return {
    c() {
      e = Qn("svg"), t = Qn("g"), i = Qn("path"), l = Qn("path"), this.h();
    },
    l(o) {
      e = Jn(o, "svg", {
        width: !0,
        height: !0,
        viewBox: !0,
        version: !0,
        xmlns: !0,
        "xmlns:xlink": !0,
        "xml:space": !0,
        stroke: !0,
        style: !0
      });
      var a = Kn(e);
      t = Jn(a, "g", { transform: !0 });
      var s = Kn(t);
      i = Jn(s, "path", { d: !0, style: !0 }), Kn(i).forEach(Dn), s.forEach(Dn), l = Jn(a, "path", { d: !0, style: !0 }), Kn(l).forEach(Dn), a.forEach(Dn), this.h();
    },
    h() {
      et(i, "d", "M18,6L6.087,17.913"), ct(i, "fill", "none"), ct(i, "fill-rule", "nonzero"), ct(i, "stroke-width", "2px"), et(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), et(l, "d", "M4.364,4.364L19.636,19.636"), ct(l, "fill", "none"), ct(l, "fill-rule", "nonzero"), ct(l, "stroke-width", "2px"), et(e, "width", "100%"), et(e, "height", "100%"), et(e, "viewBox", "0 0 24 24"), et(e, "version", "1.1"), et(e, "xmlns", "http://www.w3.org/2000/svg"), et(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), et(e, "xml:space", "preserve"), et(e, "stroke", "currentColor"), ct(e, "fill-rule", "evenodd"), ct(e, "clip-rule", "evenodd"), ct(e, "stroke-linecap", "round"), ct(e, "stroke-linejoin", "round");
    },
    m(o, a) {
      gr(o, e, a), vi(e, t), vi(t, i), vi(e, l);
    },
    p: ki,
    i: ki,
    o: ki,
    d(o) {
      o && Dn(e);
    }
  };
}
class wr extends mr {
  constructor(e) {
    super(), hr(this, e, null, pr, br, {});
  }
}
const vr = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], yl = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
vr.reduce(
  (n, { color: e, primary: t, secondary: i }) => ({
    ...n,
    [e]: {
      primary: yl[e][t],
      secondary: yl[e][i]
    }
  }),
  {}
);
const { tick: kr } = window.__gradio__svelte__internal;
async function Bi(n, e, t, i) {
  if (await kr(), i || e === t) return;
  const l = window.getComputedStyle(n), o = parseFloat(l.paddingTop), a = parseFloat(l.paddingBottom), s = parseFloat(l.lineHeight);
  let r = t === void 0 ? !1 : o + a + s * t, f = o + a + e * s;
  n.style.height = "1px";
  let _;
  r && n.scrollHeight > r ? _ = r : n.scrollHeight < f ? _ = f : _ = n.scrollHeight, n.style.height = `${_}px`;
}
function yr(n, e) {
  if (e.lines === e.max_lines) return;
  n.style.overflowY = "scroll";
  function t(i) {
    Bi(i.target, e.lines, e.max_lines, !1);
  }
  if (n.addEventListener("input", t), !!e.text.trim())
    return Bi(n, e.lines, e.max_lines, !1), {
      destroy: () => n.removeEventListener("input", t)
    };
}
function Er(n, e) {
  return n.addEventListener(
    "icegatheringstatechange",
    () => {
      console.debug(n.iceGatheringState);
    },
    !1
  ), n.addEventListener(
    "iceconnectionstatechange",
    () => {
      console.debug(n.iceConnectionState);
    },
    !1
  ), n.addEventListener(
    "signalingstatechange",
    () => {
      console.debug(n.signalingState);
    },
    !1
  ), n.addEventListener("track", (t) => {
    console.debug("track event listener"), e && e.srcObject !== t.streams[0] && (console.debug("streams", t.streams), e.srcObject = t.streams[0], console.debug("node.srcOject", e.srcObject), t.track.kind === "audio" && (e.volume = 1, e.muted = !1, e.autoplay = !0, console.debug(e), console.debug("autoplay track"), e.play().catch((i) => console.debug("Autoplay failed:", i))));
  }), n;
}
async function Tr(n, e, t, i, l, o = "video", a = () => {
}, s = {}) {
  e = Er(e, t);
  const r = e.createDataChannel("text");
  return r.onopen = () => {
    console.debug("Data channel is open"), r.send("handshake");
  }, r.onmessage = (f) => {
    console.debug("Received message:", f.data), (f.data === "change" || f.data === "tick" || f.data === "stopword") && (console.debug(`${f.data} event received`), console.debug(`${f}`), a(f.data));
  }, n ? n.getTracks().forEach(async (f) => {
    console.debug("Track stream callback", f);
    const _ = e.addTrack(f, n), c = { ..._.getParameters(), ...s };
    await _.setParameters(c), console.debug("sender params", _.getParameters());
  }) : (console.debug("Creating transceiver!"), e.addTransceiver(o, { direction: "recvonly" })), await Sr(e, i, l), e;
}
function Ar(n, e) {
  return new Promise((t, i) => {
    n(e).then((l) => {
      console.debug("data", l), (l == null ? void 0 : l.status) === "failed" && (console.debug("rejecting"), i("error")), t(l);
    });
  });
}
async function Sr(n, e, t) {
  return n.createOffer().then((i) => n.setLocalDescription(i)).then(() => new Promise((i) => {
    if (console.debug("ice gathering state", n.iceGatheringState), n.iceGatheringState === "complete")
      i();
    else {
      const l = () => {
        n.iceGatheringState === "complete" && (console.debug("ice complete"), n.removeEventListener("icegatheringstatechange", l), i());
      };
      n.addEventListener("icegatheringstatechange", l);
    }
  })).then(() => {
    var i = n.localDescription;
    return Ar(e, {
      sdp: i.sdp,
      type: i.type,
      webrtc_id: t
    });
  }).then((i) => i).then((i) => n.setRemoteDescription(i));
}
function El(n) {
  console.debug("Stopping peer connection"), n.getTransceivers && n.getTransceivers().forEach((e) => {
    e.stop && e.stop();
  }), n.getSenders() && n.getSenders().forEach((e) => {
    console.debug("sender", e), e.track && e.track.stop && e.track.stop();
  }), setTimeout(() => {
    n.close();
  }, 500);
}
function Dr() {
  return navigator.mediaDevices.enumerateDevices();
}
function Lr(n, e = "videoinput") {
  return n.filter(
    (i) => i.kind === e
  );
}
const {
  SvelteComponent: Cr,
  append_hydration: yi,
  attr: _t,
  children: bn,
  claim_element: Kt,
  claim_space: Ir,
  destroy_each: Co,
  detach: Ke,
  element: Jt,
  empty: Tl,
  ensure_array_like: fi,
  init: Nr,
  insert_hydration: kn,
  noop: Hi,
  safe_not_equal: Or,
  set_style: ht,
  space: Rr,
  src_url_equal: Al
} = window.__gradio__svelte__internal, { onDestroy: Mr } = window.__gradio__svelte__internal;
function Sl(n, e, t) {
  const i = n.slice();
  return i[17] = e[t], i;
}
function Dl(n, e, t) {
  const i = n.slice();
  return i[17] = e[t], i[19] = t, i;
}
function Pr(n) {
  let e, t = fi(Array(
    /*numBars*/
    n[0]
  )), i = [];
  for (let l = 0; l < t.length; l += 1)
    i[l] = Ll(Sl(n, t, l));
  return {
    c() {
      e = Jt("div");
      for (let l = 0; l < i.length; l += 1)
        i[l].c();
      this.h();
    },
    l(l) {
      e = Kt(l, "DIV", { class: !0 });
      var o = bn(e);
      for (let a = 0; a < i.length; a += 1)
        i[a].l(o);
      o.forEach(Ke), this.h();
    },
    h() {
      _t(e, "class", "gradio-audio-boxContainer svelte-1cqbdpi"), ht(
        e,
        "width",
        /*containerWidth*/
        n[6]
      );
    },
    m(l, o) {
      kn(l, e, o);
      for (let a = 0; a < i.length; a += 1)
        i[a] && i[a].m(e, null);
    },
    p(l, o) {
      if (o & /*numBars*/
      1) {
        t = fi(Array(
          /*numBars*/
          l[0]
        ));
        let a;
        for (a = 0; a < t.length; a += 1) {
          const s = Sl(l, t, a);
          i[a] ? i[a].p(s, o) : (i[a] = Ll(), i[a].c(), i[a].m(e, null));
        }
        for (; a < i.length; a += 1)
          i[a].d(1);
        i.length = t.length;
      }
      o & /*containerWidth*/
      64 && ht(
        e,
        "width",
        /*containerWidth*/
        l[6]
      );
    },
    d(l) {
      l && Ke(e), Co(i, l);
    }
  };
}
function Fr(n) {
  let e, t, i, l, o, a = (
    /*pulseIntensity*/
    n[5] > 0 && Cl(n)
  );
  return {
    c() {
      e = Jt("div"), a && a.c(), t = Rr(), i = Jt("div"), l = Jt("img"), this.h();
    },
    l(s) {
      e = Kt(s, "DIV", { class: !0 });
      var r = bn(e);
      a && a.l(r), t = Ir(r), i = Kt(r, "DIV", { class: !0 });
      var f = bn(i);
      l = Kt(f, "IMG", { src: !0, alt: !0, class: !0 }), f.forEach(Ke), r.forEach(Ke), this.h();
    },
    h() {
      Al(l.src, o = /*icon*/
      n[1]) || _t(l, "src", o), _t(l, "alt", "Audio visualization icon"), _t(l, "class", "icon-image svelte-1cqbdpi"), _t(i, "class", "gradio-audio-icon svelte-1cqbdpi"), ht(i, "transform", `scale(${/*pulseScale*/
      n[4]})`), ht(
        i,
        "background",
        /*icon_button_color*/
        n[2]
      ), _t(e, "class", "gradio-audio-icon-container svelte-1cqbdpi");
    },
    m(s, r) {
      kn(s, e, r), a && a.m(e, null), yi(e, t), yi(e, i), yi(i, l);
    },
    p(s, r) {
      /*pulseIntensity*/
      s[5] > 0 ? a ? a.p(s, r) : (a = Cl(s), a.c(), a.m(e, t)) : a && (a.d(1), a = null), r & /*icon*/
      2 && !Al(l.src, o = /*icon*/
      s[1]) && _t(l, "src", o), r & /*pulseScale*/
      16 && ht(i, "transform", `scale(${/*pulseScale*/
      s[4]})`), r & /*icon_button_color*/
      4 && ht(
        i,
        "background",
        /*icon_button_color*/
        s[2]
      );
    },
    d(s) {
      s && Ke(e), a && a.d();
    }
  };
}
function Ll(n) {
  let e;
  return {
    c() {
      e = Jt("div"), this.h();
    },
    l(t) {
      e = Kt(t, "DIV", { class: !0, style: !0 }), bn(e).forEach(Ke), this.h();
    },
    h() {
      _t(e, "class", "gradio-audio-box svelte-1cqbdpi"), ht(e, "transform", "scaleY(0.1)");
    },
    m(t, i) {
      kn(t, e, i);
    },
    p: Hi,
    d(t) {
      t && Ke(e);
    }
  };
}
function Cl(n) {
  let e, t = fi(Array(3)), i = [];
  for (let l = 0; l < t.length; l += 1)
    i[l] = Il(Dl(n, t, l));
  return {
    c() {
      for (let l = 0; l < i.length; l += 1)
        i[l].c();
      e = Tl();
    },
    l(l) {
      for (let o = 0; o < i.length; o += 1)
        i[o].l(l);
      e = Tl();
    },
    m(l, o) {
      for (let a = 0; a < i.length; a += 1)
        i[a] && i[a].m(l, o);
      kn(l, e, o);
    },
    p(l, o) {
      if (o & /*pulse_color*/
      8) {
        t = fi(Array(3));
        let a;
        for (a = 0; a < t.length; a += 1) {
          const s = Dl(l, t, a);
          i[a] ? i[a].p(s, o) : (i[a] = Il(s), i[a].c(), i[a].m(e.parentNode, e));
        }
        for (; a < i.length; a += 1)
          i[a].d(1);
        i.length = t.length;
      }
    },
    d(l) {
      l && Ke(e), Co(i, l);
    }
  };
}
function Il(n) {
  let e;
  return {
    c() {
      e = Jt("div"), this.h();
    },
    l(t) {
      e = Kt(t, "DIV", { class: !0 }), bn(e).forEach(Ke), this.h();
    },
    h() {
      _t(e, "class", "pulse-ring svelte-1cqbdpi"), ht(
        e,
        "background",
        /*pulse_color*/
        n[3]
      ), ht(e, "animation-delay", `${/*i*/
      n[19] * 0.4}s`);
    },
    m(t, i) {
      kn(t, e, i);
    },
    p(t, i) {
      i & /*pulse_color*/
      8 && ht(
        e,
        "background",
        /*pulse_color*/
        t[3]
      );
    },
    d(t) {
      t && Ke(e);
    }
  };
}
function Ur(n) {
  let e;
  function t(o, a) {
    return (
      /*icon*/
      o[1] ? Fr : Pr
    );
  }
  let i = t(n), l = i(n);
  return {
    c() {
      e = Jt("div"), l.c(), this.h();
    },
    l(o) {
      e = Kt(o, "DIV", { class: !0 });
      var a = bn(e);
      l.l(a), a.forEach(Ke), this.h();
    },
    h() {
      _t(e, "class", "gradio-audio-waveContainer svelte-1cqbdpi");
    },
    m(o, a) {
      kn(o, e, a), l.m(e, null);
    },
    p(o, [a]) {
      i === (i = t(o)) && l ? l.p(o, a) : (l.d(1), l = i(o), l && (l.c(), l.m(e, null)));
    },
    i: Hi,
    o: Hi,
    d(o) {
      o && Ke(e), l.d();
    }
  };
}
function zr(n, e, t) {
  let i;
  var l = this && this.__awaiter || function(b, O, P, U) {
    function j(F) {
      return F instanceof P ? F : new P(function(L) {
        L(F);
      });
    }
    return new (P || (P = Promise))(function(F, L) {
      function J(B) {
        try {
          ne(U.next(B));
        } catch (ie) {
          L(ie);
        }
      }
      function Y(B) {
        try {
          ne(U.throw(B));
        } catch (ie) {
          L(ie);
        }
      }
      function ne(B) {
        B.done ? F(B.value) : j(B.value).then(J, Y);
      }
      ne((U = U.apply(b, O || [])).next());
    });
  };
  let { numBars: o = 16 } = e, { stream_state: a = "closed" } = e, { audio_source_callback: s } = e, { icon: r = void 0 } = e, { icon_button_color: f = "var(--body-text-color)" } = e, { pulse_color: _ = "var(--body-text-color)" } = e, d, c, u, h, v = 1, T = 0;
  Mr(() => {
    h && cancelAnimationFrame(h), d && d.close();
  });
  function k() {
    return l(this, void 0, void 0, function* () {
      const b = new (window.AudioContext || window.webkitAudioContext)(), O = yield navigator.mediaDevices.getUserMedia({ audio: !0 }), P = yield s(), U = b.createMediaStreamSource(O), j = b.createMediaStreamSource(P), F = b.createMediaStreamDestination();
      return U.connect(F), j.connect(F), F.stream;
    });
  }
  function w() {
    return l(this, void 0, void 0, function* () {
      d = new (window.AudioContext || window.webkitAudioContext)(), c = d.createAnalyser();
      const b = yield k();
      d.createMediaStreamSource(b).connect(c), c.fftSize = 64, c.smoothingTimeConstant = 0.8, u = new Uint8Array(c.frequencyBinCount), g();
    });
  }
  function g() {
    if (c.getByteFrequencyData(u), r) {
      const O = Array.from(u).reduce((P, U) => P + U, 0) / u.length / 255;
      t(4, v = 1 + O * 0.15), t(5, T = O);
    } else {
      const b = document.querySelectorAll(".gradio-audio-waveContainer .gradio-audio-box");
      for (let O = 0; O < b.length; O++) {
        const P = u[O] / 255;
        b[O].style.transform = `scaleY(${Math.max(0.1, P)})`;
      }
    }
    h = requestAnimationFrame(g);
  }
  return n.$$set = (b) => {
    "numBars" in b && t(0, o = b.numBars), "stream_state" in b && t(7, a = b.stream_state), "audio_source_callback" in b && t(8, s = b.audio_source_callback), "icon" in b && t(1, r = b.icon), "icon_button_color" in b && t(2, f = b.icon_button_color), "pulse_color" in b && t(3, _ = b.pulse_color);
  }, n.$$.update = () => {
    n.$$.dirty & /*icon, numBars*/
    3 && t(6, i = r ? "128px" : `calc((var(--boxSize) + var(--gutter)) * ${o})`), n.$$.dirty & /*stream_state*/
    128 && a === "open" && w();
  }, [
    o,
    r,
    f,
    _,
    v,
    T,
    i,
    a,
    s
  ];
}
class qr extends Cr {
  constructor(e) {
    super(), Nr(this, e, zr, Ur, Or, {
      numBars: 0,
      stream_state: 7,
      audio_source_callback: 8,
      icon: 1,
      icon_button_color: 2,
      pulse_color: 3
    });
  }
}
const {
  SvelteComponent: Br,
  append_hydration: It,
  attr: W,
  binding_callbacks: Nl,
  check_outros: Io,
  children: ot,
  claim_component: Hr,
  claim_element: pn,
  claim_space: No,
  claim_svg_element: cn,
  create_component: Wr,
  destroy_component: Vr,
  detach: Ee,
  element: wn,
  get_svelte_dataset: Gr,
  group_outros: Oo,
  init: jr,
  insert_hydration: vn,
  listen: ui,
  mount_component: Yr,
  noop: Un,
  run_all: Xr,
  safe_not_equal: Zr,
  space: Ro,
  svg_element: _n,
  toggle_class: ci,
  transition_in: qn,
  transition_out: Bn
} = window.__gradio__svelte__internal, { createEventDispatcher: Kr, onMount: Jr } = window.__gradio__svelte__internal;
function Qr(n) {
  let e, t, i, l, o, a, s, r, f;
  const _ = [es, $r], d = [];
  function c(u, h) {
    return (
      /*stream_state*/
      u[8] === "open" ? 0 : 1
    );
  }
  return e = c(n), t = d[e] = _[e](n), {
    c() {
      t.c(), i = Ro(), l = wn("button"), o = _n("svg"), a = _n("rect"), this.h();
    },
    l(u) {
      t.l(u), i = No(u), l = pn(u, "BUTTON", { class: !0, title: !0 });
      var h = ot(l);
      o = cn(h, "svg", {
        xmlns: !0,
        width: !0,
        height: !0,
        viewBox: !0,
        "stroke-linecap": !0,
        "stroke-linejoin": !0,
        class: !0
      });
      var v = ot(o);
      a = cn(v, "rect", {
        x: !0,
        y: !0,
        width: !0,
        height: !0,
        rx: !0,
        ry: !0
      }), ot(a).forEach(Ee), v.forEach(Ee), h.forEach(Ee), this.h();
    },
    h() {
      W(a, "x", "8"), W(a, "y", "8"), W(a, "width", "8"), W(a, "height", "8"), W(a, "rx", "1"), W(a, "ry", "1"), W(o, "xmlns", "http://www.w3.org/2000/svg"), W(o, "width", "100%"), W(o, "height", "100%"), W(o, "viewBox", "0 0 24 24"), W(o, "stroke-linecap", "round"), W(o, "stroke-linejoin", "round"), W(o, "class", "svelte-1qas4up"), W(l, "class", "stop-audio-button svelte-1qas4up"), W(
        l,
        "title",
        /*stop_audio_btn_title*/
        n[6]
      ), l.disabled = /*disabled*/
      n[7];
    },
    m(u, h) {
      d[e].m(u, h), vn(u, i, h), vn(u, l, h), It(l, o), It(o, a), s = !0, r || (f = ui(
        l,
        "click",
        /*handle_end_streaming_click*/
        n[14]
      ), r = !0);
    },
    p(u, h) {
      let v = e;
      e = c(u), e === v ? d[e].p(u, h) : (Oo(), Bn(d[v], 1, 1, () => {
        d[v] = null;
      }), Io(), t = d[e], t ? t.p(u, h) : (t = d[e] = _[e](u), t.c()), qn(t, 1), t.m(i.parentNode, i)), (!s || h[0] & /*stop_audio_btn_title*/
      64) && W(
        l,
        "title",
        /*stop_audio_btn_title*/
        u[6]
      ), (!s || h[0] & /*disabled*/
      128) && (l.disabled = /*disabled*/
      u[7]);
    },
    i(u) {
      s || (qn(t), s = !0);
    },
    o(u) {
      Bn(t), s = !1;
    },
    d(u) {
      u && (Ee(i), Ee(l)), d[e].d(u), r = !1, f();
    }
  };
}
function xr(n) {
  let e, t, i, l, o, a, s;
  return {
    c() {
      e = wn("button"), t = _n("svg"), i = _n("path"), l = _n("path"), o = _n("line"), this.h();
    },
    l(r) {
      e = pn(r, "BUTTON", { class: !0, title: !0 });
      var f = ot(e);
      t = cn(f, "svg", {
        xmlns: !0,
        width: !0,
        height: !0,
        viewBox: !0,
        fill: !0,
        stroke: !0,
        "stroke-width": !0,
        "stroke-linecap": !0,
        "stroke-linejoin": !0
      });
      var _ = ot(t);
      i = cn(_, "path", { d: !0 }), ot(i).forEach(Ee), l = cn(_, "path", { d: !0 }), ot(l).forEach(Ee), o = cn(_, "line", { x1: !0, x2: !0, y1: !0, y2: !0 }), ot(o).forEach(Ee), _.forEach(Ee), f.forEach(Ee), this.h();
    },
    h() {
      W(i, "d", "M12 4a2.4 2.4 0 0 0-2.4 2.4v5.6a2.4 2.4 0 0 0 4.8 0V6.4a2.4 2.4 0 0 0-2.4-2.4Z"), W(l, "d", "M17.6 10.4v1.6a5.6 5.6 0 0 1-11.2 0v-1.6"), W(o, "x1", "12"), W(o, "x2", "12"), W(o, "y1", "17.6"), W(o, "y2", "20"), W(t, "xmlns", "http://www.w3.org/2000/svg"), W(t, "width", "100%"), W(t, "height", "100%"), W(t, "viewBox", "0 0 24 24"), W(t, "fill", "none"), W(t, "stroke", "currentColor"), W(t, "stroke-width", "1.5"), W(t, "stroke-linecap", "round"), W(t, "stroke-linejoin", "round"), W(e, "class", "audio-button svelte-1qas4up"), W(
        e,
        "title",
        /*audio_btn_title*/
        n[5]
      ), e.disabled = /*disabled*/
      n[7], ci(
        e,
        "padded-button",
        /*audio_btn*/
        n[4] !== !0
      );
    },
    m(r, f) {
      vn(r, e, f), It(e, t), It(t, i), It(t, l), It(t, o), a || (s = ui(
        e,
        "click",
        /*handle_audio_click*/
        n[13]
      ), a = !0);
    },
    p(r, f) {
      f[0] & /*audio_btn_title*/
      32 && W(
        e,
        "title",
        /*audio_btn_title*/
        r[5]
      ), f[0] & /*disabled*/
      128 && (e.disabled = /*disabled*/
      r[7]), f[0] & /*audio_btn*/
      16 && ci(
        e,
        "padded-button",
        /*audio_btn*/
        r[4] !== !0
      );
    },
    i: Un,
    o: Un,
    d(r) {
      r && Ee(e), a = !1, s();
    }
  };
}
function $r(n) {
  let e, t = '<span class="svelte-1qas4up">·</span><span class="svelte-1qas4up">·</span><span class="svelte-1qas4up">·</span>';
  return {
    c() {
      e = wn("div"), e.innerHTML = t, this.h();
    },
    l(i) {
      e = pn(i, "DIV", { class: !0, "data-svelte-h": !0 }), Gr(e) !== "svelte-y8y9ab" && (e.innerHTML = t), this.h();
    },
    h() {
      W(e, "class", "audio-blinker svelte-1qas4up");
    },
    m(i, l) {
      vn(i, e, l);
    },
    p: Un,
    i: Un,
    o: Un,
    d(i) {
      i && Ee(e);
    }
  };
}
function es(n) {
  let e, t, i;
  return t = new qr({
    props: {
      audio_source_callback: (
        /*audio_source_callback*/
        n[11]
      ),
      stream_state: (
        /*stream_state*/
        n[8]
      ),
      icon: (
        /*icon*/
        n[1]
      ),
      icon_button_color: (
        /*icon_button_color*/
        n[2]
      ),
      pulse_color: (
        /*pulse_color*/
        n[3]
      )
    }
  }), {
    c() {
      e = wn("div"), Wr(t.$$.fragment), this.h();
    },
    l(l) {
      e = pn(l, "DIV", { class: !0 });
      var o = ot(e);
      Hr(t.$$.fragment, o), o.forEach(Ee), this.h();
    },
    h() {
      W(e, "class", "audiowave svelte-1qas4up");
    },
    m(l, o) {
      vn(l, e, o), Yr(t, e, null), i = !0;
    },
    p(l, o) {
      const a = {};
      o[0] & /*stream_state*/
      256 && (a.stream_state = /*stream_state*/
      l[8]), o[0] & /*icon*/
      2 && (a.icon = /*icon*/
      l[1]), o[0] & /*icon_button_color*/
      4 && (a.icon_button_color = /*icon_button_color*/
      l[2]), o[0] & /*pulse_color*/
      8 && (a.pulse_color = /*pulse_color*/
      l[3]), t.$set(a);
    },
    i(l) {
      i || (qn(t.$$.fragment, l), i = !0);
    },
    o(l) {
      Bn(t.$$.fragment, l), i = !1;
    },
    d(l) {
      l && Ee(e), Vr(t);
    }
  };
}
function ts(n) {
  let e, t, i, l, o, a, s, r, f;
  const _ = [xr, Qr], d = [];
  function c(u, h) {
    return (
      /*audio_btn*/
      u[4] ? 0 : (
        /*stream_state*/
        u[8] === "open" || /*stream_state*/
        u[8] === "waiting" ? 1 : -1
      )
    );
  }
  return ~(l = c(n)) && (o = d[l] = _[l](n)), {
    c() {
      e = wn("div"), t = wn("audio"), i = Ro(), o && o.c(), this.h();
    },
    l(u) {
      e = pn(u, "DIV", { class: !0 });
      var h = ot(e);
      t = pn(h, "AUDIO", { class: !0 }), ot(t).forEach(Ee), i = No(h), o && o.l(h), h.forEach(Ee), this.h();
    },
    h() {
      W(t, "class", "standard-player svelte-1qas4up"), ci(
        t,
        "hidden",
        /*value*/
        n[0] === "__webrtc_value__"
      ), W(e, "class", a = "audio-container" + /*audio_btn*/
      (n[4] ? "" : " large") + " svelte-1qas4up");
    },
    m(u, h) {
      vn(u, e, h), It(e, t), n[27](t), It(e, i), ~l && d[l].m(e, null), n[30](e), s = !0, r || (f = [
        ui(
          t,
          "ended",
          /*ended_handler*/
          n[28]
        ),
        ui(
          t,
          "play",
          /*play_handler*/
          n[29]
        )
      ], r = !0);
    },
    p(u, h) {
      (!s || h[0] & /*value*/
      1) && ci(
        t,
        "hidden",
        /*value*/
        u[0] === "__webrtc_value__"
      );
      let v = l;
      l = c(u), l === v ? ~l && d[l].p(u, h) : (o && (Oo(), Bn(d[v], 1, 1, () => {
        d[v] = null;
      }), Io()), ~l ? (o = d[l], o ? o.p(u, h) : (o = d[l] = _[l](u), o.c()), qn(o, 1), o.m(e, null)) : o = null), (!s || h[0] & /*audio_btn*/
      16 && a !== (a = "audio-container" + /*audio_btn*/
      (u[4] ? "" : " large") + " svelte-1qas4up")) && W(e, "class", a);
    },
    i(u) {
      s || (qn(o), s = !0);
    },
    o(u) {
      Bn(o), s = !1;
    },
    d(u) {
      u && Ee(e), n[27](null), ~l && d[l].d(), n[30](null), r = !1, Xr(f);
    }
  };
}
function ns(n, e, t) {
  var i = this && this.__awaiter || function(D, Z, ee, y) {
    function M(H) {
      return H instanceof ee ? H : new ee(function(q) {
        q(H);
      });
    }
    return new (ee || (ee = Promise))(function(H, q) {
      function x(me) {
        try {
          _e(y.next(me));
        } catch (Ae) {
          q(Ae);
        }
      }
      function ce(me) {
        try {
          _e(y.throw(me));
        } catch (Ae) {
          q(Ae);
        }
      }
      function _e(me) {
        me.done ? H(me.value) : M(me.value).then(x, ce);
      }
      _e((y = y.apply(D, Z || [])).next());
    });
  };
  let { mode: l } = e, { value: o = null } = e, { rtc_configuration: a = null } = e, { i18n: s } = e, { time_limit: r = null } = e, { track_constraints: f = {} } = e, { rtp_params: _ = {} } = e, { on_change_cb: d } = e, { icon: c = void 0 } = e, { icon_button_color: u = "var(--body-text-color)" } = e, { pulse_color: h = "var(--body-text-color)" } = e, { audio_btn: v = !1 } = e, { audio_btn_title: T = "" } = e, { handle_audio_click_visibility: k = function() {
  } } = e, { stop_audio_btn_title: w = "" } = e, { handle_end_streaming_click_visibility: g = function() {
  } } = e, { disabled: b = !1 } = e, O = !1, P;
  Jr(() => {
    o === "__webrtc_value__" && t(26, P = new Audio("https://huggingface.co/datasets/freddyaboulton/bucket/resolve/main/pop-sounds.mp3"));
  });
  let U = (D) => {
    D === "stopword" ? (console.log("stopword recognized"), t(25, O = !0), setTimeout(
      () => {
        t(25, O = !1);
      },
      3e3
    )) : d(D);
  }, { server: j } = e, F = "closed", L, J, Y, ne = null, B, ie, se = null;
  const Oe = () => (console.log("stream in callback", B), l === "send" ? B : L.srcObject), de = Kr();
  function be() {
    return i(this, void 0, void 0, function* () {
      try {
        const Z = se ? Object.assign(
          {
            deviceId: { exact: se.deviceId }
          },
          f
        ) : f;
        B = yield navigator.mediaDevices.getUserMedia({ audio: Z });
      } catch (Z) {
        if (!navigator.mediaDevices) {
          de("error", s("audio.no_device_support"));
          return;
        }
        if (Z instanceof DOMException && Z.name == "NotAllowedError") {
          de("error", s("audio.allow_recording_access"));
          return;
        }
        throw Z;
      }
      ie = Lr(yield Dr(), "audioinput");
      const D = B.getTracks().map((Z) => {
        var ee;
        return (ee = Z.getSettings()) === null || ee === void 0 ? void 0 : ee.deviceId;
      })[0];
      se = D && ie.find((Z) => Z.deviceId === D) || ie[0];
    });
  }
  function Le() {
    return i(this, void 0, void 0, function* () {
      B && (B.getTracks().forEach((D) => D.stop()), B = null);
    });
  }
  function K() {
    return i(this, void 0, void 0, function* () {
      if (F === "open" || F === "waiting") {
        t(8, F = "waiting"), El(Y), yield be(), yield Le(), t(8, F = "closed");
        return;
      }
      t(8, F = "waiting"), ne = Math.random().toString(36).substring(2), t(0, o = ne), console.log(o), Y = new RTCPeerConnection(a), Y.addEventListener("connectionstatechange", (D) => i(this, void 0, void 0, function* () {
        switch (Y.connectionState) {
          case "connected":
            console.info("connected"), t(8, F = "open");
            break;
          case "disconnected":
            console.info("closed"), t(8, F = "closed"), El(Y);
            break;
        }
      })), B = null;
      try {
        yield be();
      } catch (D) {
        if (!navigator.mediaDevices) {
          de("error", s("audio.no_device_support"));
          return;
        }
        if (D instanceof DOMException && D.name == "NotAllowedError") {
          de("error", s("audio.allow_recording_access"));
          return;
        }
        throw D;
      }
      B != null && Tr(B, Y, l === "send" ? null : L, j.offer, ne, "audio", U, _).then((D) => {
        Y = D;
      }).catch((D) => {
        console.error("interactive audio error: ", D);
      });
    });
  }
  function ve() {
    k(), K();
  }
  function X() {
    g(), F === "open" || F === "waiting" ? K() : t(8, F = "closed");
  }
  function le(D) {
    Nl[D ? "unshift" : "push"](() => {
      L = D, t(9, L);
    });
  }
  const S = () => de("stop"), Te = () => de("play");
  function pe(D) {
    Nl[D ? "unshift" : "push"](() => {
      J = D, t(10, J);
    });
  }
  return n.$$set = (D) => {
    "mode" in D && t(15, l = D.mode), "value" in D && t(0, o = D.value), "rtc_configuration" in D && t(16, a = D.rtc_configuration), "i18n" in D && t(17, s = D.i18n), "time_limit" in D && t(18, r = D.time_limit), "track_constraints" in D && t(19, f = D.track_constraints), "rtp_params" in D && t(20, _ = D.rtp_params), "on_change_cb" in D && t(21, d = D.on_change_cb), "icon" in D && t(1, c = D.icon), "icon_button_color" in D && t(2, u = D.icon_button_color), "pulse_color" in D && t(3, h = D.pulse_color), "audio_btn" in D && t(4, v = D.audio_btn), "audio_btn_title" in D && t(5, T = D.audio_btn_title), "handle_audio_click_visibility" in D && t(22, k = D.handle_audio_click_visibility), "stop_audio_btn_title" in D && t(6, w = D.stop_audio_btn_title), "handle_end_streaming_click_visibility" in D && t(23, g = D.handle_end_streaming_click_visibility), "disabled" in D && t(7, b = D.disabled), "server" in D && t(24, j = D.server);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*stopword_recognized, notification_sound*/
    100663296 && O && P.play();
  }, [
    o,
    c,
    u,
    h,
    v,
    T,
    w,
    b,
    F,
    L,
    J,
    Oe,
    de,
    ve,
    X,
    l,
    a,
    s,
    r,
    f,
    _,
    d,
    k,
    g,
    j,
    O,
    P,
    le,
    S,
    Te,
    pe
  ];
}
class is extends Br {
  constructor(e) {
    super(), jr(
      this,
      e,
      ns,
      ts,
      Zr,
      {
        mode: 15,
        value: 0,
        rtc_configuration: 16,
        i18n: 17,
        time_limit: 18,
        track_constraints: 19,
        rtp_params: 20,
        on_change_cb: 21,
        icon: 1,
        icon_button_color: 2,
        pulse_color: 3,
        audio_btn: 4,
        audio_btn_title: 5,
        handle_audio_click_visibility: 22,
        stop_audio_btn_title: 6,
        handle_end_streaming_click_visibility: 23,
        disabled: 7,
        server: 24
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: ls,
  action_destroyer: os,
  add_flush_callback: ii,
  append_hydration: We,
  attr: N,
  bind: li,
  binding_callbacks: Qt,
  bubble: xn,
  check_outros: Wi,
  children: ze,
  claim_component: Mo,
  claim_element: Yt,
  claim_space: Mn,
  claim_svg_element: xt,
  claim_text: as,
  create_component: Po,
  destroy_component: Fo,
  detach: ue,
  element: Xt,
  empty: Ol,
  group_outros: Vi,
  init: rs,
  insert_hydration: Mt,
  is_function: ss,
  listen: Fe,
  mount_component: Uo,
  noop: Ct,
  prevent_default: fs,
  run_all: us,
  safe_not_equal: cs,
  set_data: _s,
  set_input_value: Rl,
  space: Pn,
  svg_element: $t,
  text: ds,
  toggle_class: dt,
  transition_in: mt,
  transition_out: Nt
} = window.__gradio__svelte__internal, { beforeUpdate: ms, afterUpdate: hs, createEventDispatcher: gs, tick: Ml } = window.__gradio__svelte__internal;
function Pl(n) {
  let e, t, i, l, o, a, s, r, f, _;
  function d(w) {
    n[66](w);
  }
  function c(w) {
    n[67](w);
  }
  function u(w) {
    n[68](w);
  }
  let h = {
    file_count: (
      /*file_count*/
      n[19]
    ),
    filetype: (
      /*file_types*/
      n[15]
    ),
    root: (
      /*root*/
      n[14]
    ),
    max_file_size: (
      /*max_file_size*/
      n[16]
    ),
    show_progress: !1,
    disable_click: !0,
    hidden: !0,
    upload: (
      /*upload*/
      n[17]
    ),
    stream_handler: (
      /*stream_handler*/
      n[18]
    )
  };
  /*dragging*/
  n[2] !== void 0 && (h.dragging = /*dragging*/
  n[2]), /*uploading*/
  n[32] !== void 0 && (h.uploading = /*uploading*/
  n[32]), /*hidden_upload*/
  n[35] !== void 0 && (h.hidden_upload = /*hidden_upload*/
  n[35]), e = new Ma({ props: h }), n[65](e), Qt.push(() => li(e, "dragging", d)), Qt.push(() => li(e, "uploading", c)), Qt.push(() => li(e, "hidden_upload", u)), e.$on(
    "load",
    /*handle_upload*/
    n[45]
  ), e.$on(
    "error",
    /*error_handler*/
    n[69]
  );
  function v(w, g) {
    return (
      /*upload_btn*/
      w[8] === !0 ? ps : bs
    );
  }
  let T = v(n), k = T(n);
  return {
    c() {
      Po(e.$$.fragment), o = Pn(), a = Xt("button"), k.c(), this.h();
    },
    l(w) {
      Mo(e.$$.fragment, w), o = Mn(w), a = Yt(w, "BUTTON", {
        "data-testid": !0,
        class: !0,
        title: !0,
        style: !0
      });
      var g = ze(a);
      k.l(g), g.forEach(ue), this.h();
    },
    h() {
      N(a, "data-testid", "upload-button"), N(a, "class", "upload-button svelte-16q8wod"), N(
        a,
        "title",
        /*upload_btn_title*/
        n[37]
      ), a.disabled = /*disabled*/
      n[1], N(a, "style", s = `${/*stop_audio_btn*/
      n[21] ? "display: none;" : ""}`);
    },
    m(w, g) {
      Uo(e, w, g), Mt(w, o, g), Mt(w, a, g), k.m(a, null), r = !0, f || (_ = Fe(
        a,
        "click",
        /*handle_upload_click*/
        n[46]
      ), f = !0);
    },
    p(w, g) {
      const b = {};
      g[0] & /*file_count*/
      524288 && (b.file_count = /*file_count*/
      w[19]), g[0] & /*file_types*/
      32768 && (b.filetype = /*file_types*/
      w[15]), g[0] & /*root*/
      16384 && (b.root = /*root*/
      w[14]), g[0] & /*max_file_size*/
      65536 && (b.max_file_size = /*max_file_size*/
      w[16]), g[0] & /*upload*/
      131072 && (b.upload = /*upload*/
      w[17]), g[0] & /*stream_handler*/
      262144 && (b.stream_handler = /*stream_handler*/
      w[18]), !t && g[0] & /*dragging*/
      4 && (t = !0, b.dragging = /*dragging*/
      w[2], ii(() => t = !1)), !i && g[1] & /*uploading*/
      2 && (i = !0, b.uploading = /*uploading*/
      w[32], ii(() => i = !1)), !l && g[1] & /*hidden_upload*/
      16 && (l = !0, b.hidden_upload = /*hidden_upload*/
      w[35], ii(() => l = !1)), e.$set(b), T === (T = v(w)) && k ? k.p(w, g) : (k.d(1), k = T(w), k && (k.c(), k.m(a, null))), (!r || g[1] & /*upload_btn_title*/
      64) && N(
        a,
        "title",
        /*upload_btn_title*/
        w[37]
      ), (!r || g[0] & /*disabled*/
      2) && (a.disabled = /*disabled*/
      w[1]), (!r || g[0] & /*stop_audio_btn*/
      2097152 && s !== (s = `${/*stop_audio_btn*/
      w[21] ? "display: none;" : ""}`)) && N(a, "style", s);
    },
    i(w) {
      r || (mt(e.$$.fragment, w), r = !0);
    },
    o(w) {
      Nt(e.$$.fragment, w), r = !1;
    },
    d(w) {
      w && (ue(o), ue(a)), n[65](null), Fo(e, w), k.d(), f = !1, _();
    }
  };
}
function bs(n) {
  let e;
  return {
    c() {
      e = ds(
        /*upload_btn*/
        n[8]
      );
    },
    l(t) {
      e = as(
        t,
        /*upload_btn*/
        n[8]
      );
    },
    m(t, i) {
      Mt(t, e, i);
    },
    p(t, i) {
      i[0] & /*upload_btn*/
      256 && _s(
        e,
        /*upload_btn*/
        t[8]
      );
    },
    d(t) {
      t && ue(e);
    }
  };
}
function ps(n) {
  let e, t, i;
  return {
    c() {
      e = $t("svg"), t = $t("path"), i = $t("path"), this.h();
    },
    l(l) {
      e = xt(l, "svg", {
        xmlns: !0,
        width: !0,
        height: !0,
        viewBox: !0,
        "stroke-linecap": !0,
        "stroke-linejoin": !0
      });
      var o = ze(e);
      t = xt(o, "path", { d: !0, "stroke-width": !0 }), ze(t).forEach(ue), i = xt(o, "path", { d: !0, "stroke-width": !0 }), ze(i).forEach(ue), o.forEach(ue), this.h();
    },
    h() {
      N(t, "d", "M12 5L12 19"), N(t, "stroke-width", "1.3"), N(i, "d", "M5 12L19 12"), N(i, "stroke-width", "1.3"), N(e, "xmlns", "http://www.w3.org/2000/svg"), N(e, "width", "100%"), N(e, "height", "100%"), N(e, "viewBox", "0 0 24 24"), N(e, "stroke-linecap", "round"), N(e, "stroke-linejoin", "round");
    },
    m(l, o) {
      Mt(l, e, o), We(e, t), We(e, i);
    },
    p: Ct,
    d(l) {
      l && ue(e);
    }
  };
}
function Fl(n) {
  let e, t, i, l;
  const o = [vs, ws], a = [];
  function s(r, f) {
    return (
      /*mode*/
      (r[26] === "send-receive" || /*mode*/
      r[26] == "send") && /*modality*/
      r[25] === "video" ? 0 : (
        /*mode*/
        (r[26] === "send-receive" || /*mode*/
        r[26] === "send") && /*modality*/
        r[25] === "audio" ? 1 : -1
      )
    );
  }
  return ~(e = s(n)) && (t = a[e] = o[e](n)), {
    c() {
      t && t.c(), i = Ol();
    },
    l(r) {
      t && t.l(r), i = Ol();
    },
    m(r, f) {
      ~e && a[e].m(r, f), Mt(r, i, f), l = !0;
    },
    p(r, f) {
      let _ = e;
      e = s(r), e === _ ? ~e && a[e].p(r, f) : (t && (Vi(), Nt(a[_], 1, 1, () => {
        a[_] = null;
      }), Wi()), ~e ? (t = a[e], t ? t.p(r, f) : (t = a[e] = o[e](r), t.c()), mt(t, 1), t.m(i.parentNode, i)) : t = null);
    },
    i(r) {
      l || (mt(t), l = !0);
    },
    o(r) {
      Nt(t), l = !1;
    },
    d(r) {
      r && ue(i), ~e && a[e].d(r);
    }
  };
}
function ws(n) {
  let e, t, i;
  function l(a) {
    n[72](a);
  }
  let o = {
    mode: (
      /*mode*/
      n[26]
    ),
    rtc_configuration: (
      /*rtc_configuration*/
      n[23]
    ),
    i18n: (
      /*gradio*/
      n[22].i18n
    ),
    time_limit: (
      /*time_limit*/
      n[24]
    ),
    track_constraints: (
      /*track_constraints*/
      n[28]
    ),
    rtp_params: (
      /*rtp_params*/
      n[27]
    ),
    on_change_cb: (
      /*on_change_cb*/
      n[29]
    ),
    server: (
      /*server*/
      n[30]
    ),
    audio_btn: (
      /*audio_btn*/
      n[20]
    ),
    audio_btn_title: (
      /*audio_btn_title*/
      n[40]
    ),
    handle_audio_click_visibility: (
      /*handle_audio_click_visibility*/
      n[53]
    ),
    stop_audio_btn: (
      /*stop_audio_btn*/
      n[21]
    ),
    stop_audio_btn_title: (
      /*stop_audio_btn_title*/
      n[41]
    ),
    handle_end_streaming_click_visibility: (
      /*handle_end_streaming_click_visibility*/
      n[54]
    ),
    disabled: (
      /*disabled*/
      n[1]
    )
  };
  return (
    /*value*/
    n[0].audio !== void 0 && (o.value = /*value*/
    n[0].audio), e = new is({ props: o }), Qt.push(() => li(e, "value", l)), e.$on(
      "tick",
      /*tick_handler*/
      n[73]
    ), e.$on(
      "error",
      /*error_handler_1*/
      n[74]
    ), {
      c() {
        Po(e.$$.fragment);
      },
      l(a) {
        Mo(e.$$.fragment, a);
      },
      m(a, s) {
        Uo(e, a, s), i = !0;
      },
      p(a, s) {
        const r = {};
        s[0] & /*mode*/
        67108864 && (r.mode = /*mode*/
        a[26]), s[0] & /*rtc_configuration*/
        8388608 && (r.rtc_configuration = /*rtc_configuration*/
        a[23]), s[0] & /*gradio*/
        4194304 && (r.i18n = /*gradio*/
        a[22].i18n), s[0] & /*time_limit*/
        16777216 && (r.time_limit = /*time_limit*/
        a[24]), s[0] & /*track_constraints*/
        268435456 && (r.track_constraints = /*track_constraints*/
        a[28]), s[0] & /*rtp_params*/
        134217728 && (r.rtp_params = /*rtp_params*/
        a[27]), s[0] & /*on_change_cb*/
        536870912 && (r.on_change_cb = /*on_change_cb*/
        a[29]), s[0] & /*server*/
        1073741824 && (r.server = /*server*/
        a[30]), s[0] & /*audio_btn*/
        1048576 && (r.audio_btn = /*audio_btn*/
        a[20]), s[1] & /*audio_btn_title*/
        512 && (r.audio_btn_title = /*audio_btn_title*/
        a[40]), s[0] & /*stop_audio_btn*/
        2097152 && (r.stop_audio_btn = /*stop_audio_btn*/
        a[21]), s[1] & /*stop_audio_btn_title*/
        1024 && (r.stop_audio_btn_title = /*stop_audio_btn_title*/
        a[41]), s[0] & /*disabled*/
        2 && (r.disabled = /*disabled*/
        a[1]), !t && s[0] & /*value*/
        1 && (t = !0, r.value = /*value*/
        a[0].audio, ii(() => t = !1)), e.$set(r);
      },
      i(a) {
        i || (mt(e.$$.fragment, a), i = !0);
      },
      o(a) {
        Nt(e.$$.fragment, a), i = !1;
      },
      d(a) {
        Fo(e, a);
      }
    }
  );
}
function vs(n) {
  return {
    c: Ct,
    l: Ct,
    m: Ct,
    p: Ct,
    i: Ct,
    o: Ct,
    d: Ct
  };
}
function Ul(n) {
  let e, t, i, l, o;
  return {
    c() {
      e = Xt("button"), t = $t("svg"), i = $t("path"), this.h();
    },
    l(a) {
      e = Yt(a, "BUTTON", { class: !0, title: !0 });
      var s = ze(e);
      t = xt(s, "svg", {
        xmlns: !0,
        width: !0,
        height: !0,
        viewBox: !0
      });
      var r = ze(t);
      i = xt(r, "path", {
        d: !0,
        "stroke-width": !0,
        "stroke-linecap": !0,
        "stroke-linejoin": !0
      }), ze(i).forEach(ue), r.forEach(ue), s.forEach(ue), this.h();
    },
    h() {
      N(i, "d", "M12 5V18M12 5L7 10M12 5L17 10"), N(i, "stroke-width", "1.6"), N(i, "stroke-linecap", "round"), N(i, "stroke-linejoin", "round"), N(t, "xmlns", "http://www.w3.org/2000/svg"), N(t, "width", "100%"), N(t, "height", "100%"), N(t, "viewBox", "0 0 24 24"), N(e, "class", "submit-button svelte-16q8wod"), N(
        e,
        "title",
        /*submit_btn_title*/
        n[38]
      ), e.disabled = /*disabled*/
      n[1], dt(
        e,
        "padded-button",
        /*submit_btn*/
        n[9] !== !0
      );
    },
    m(a, s) {
      Mt(a, e, s), We(e, t), We(t, i), l || (o = Fe(
        e,
        "click",
        /*handle_submit*/
        n[48]
      ), l = !0);
    },
    p(a, s) {
      s[1] & /*submit_btn_title*/
      128 && N(
        e,
        "title",
        /*submit_btn_title*/
        a[38]
      ), s[0] & /*disabled*/
      2 && (e.disabled = /*disabled*/
      a[1]), s[0] & /*submit_btn*/
      512 && dt(
        e,
        "padded-button",
        /*submit_btn*/
        a[9] !== !0
      );
    },
    d(a) {
      a && ue(e), l = !1, o();
    }
  };
}
function zl(n) {
  let e, t, i, l, o;
  return {
    c() {
      e = Xt("button"), t = $t("svg"), i = $t("rect"), this.h();
    },
    l(a) {
      e = Yt(a, "BUTTON", { class: !0, title: !0 });
      var s = ze(e);
      t = xt(s, "svg", {
        xmlns: !0,
        width: !0,
        height: !0,
        viewBox: !0,
        "stroke-linecap": !0,
        "stroke-linejoin": !0,
        class: !0
      });
      var r = ze(t);
      i = xt(r, "rect", {
        x: !0,
        y: !0,
        width: !0,
        height: !0,
        rx: !0,
        ry: !0
      }), ze(i).forEach(ue), r.forEach(ue), s.forEach(ue), this.h();
    },
    h() {
      N(i, "x", "8"), N(i, "y", "8"), N(i, "width", "8"), N(i, "height", "8"), N(i, "rx", "1"), N(i, "ry", "1"), N(t, "xmlns", "http://www.w3.org/2000/svg"), N(t, "width", "100%"), N(t, "height", "100%"), N(t, "viewBox", "0 0 24 24"), N(t, "stroke-linecap", "round"), N(t, "stroke-linejoin", "round"), N(t, "class", "svelte-16q8wod"), N(e, "class", "stop-button svelte-16q8wod"), N(
        e,
        "title",
        /*stop_btn_title*/
        n[39]
      ), dt(
        e,
        "padded-button",
        /*stop_btn*/
        n[10] !== !0
      );
    },
    m(a, s) {
      Mt(a, e, s), We(e, t), We(t, i), l || (o = Fe(
        e,
        "click",
        /*handle_stop*/
        n[47]
      ), l = !0);
    },
    p(a, s) {
      s[1] & /*stop_btn_title*/
      256 && N(
        e,
        "title",
        /*stop_btn_title*/
        a[39]
      ), s[0] & /*stop_btn*/
      1024 && dt(
        e,
        "padded-button",
        /*stop_btn*/
        a[10] !== !0
      );
    },
    d(a) {
      a && ue(e), l = !1, o();
    }
  };
}
function ks(n) {
  let e, t, i, l, o, a, s, r, f, _, d, c, u, h, v = (
    /*upload_btn*/
    n[8] && Pl(n)
  ), T = (
    /*use_audio_video_recording*/
    n[33] && Fl(n)
  ), k = (
    /*submit_btn*/
    n[9] && Ul(n)
  ), w = (
    /*stop_btn*/
    n[10] && zl(n)
  );
  return {
    c() {
      e = Xt("div"), t = Xt("label"), i = Xt("div"), v && v.c(), l = Pn(), o = Xt("textarea"), f = Pn(), T && T.c(), _ = Pn(), k && k.c(), d = Pn(), w && w.c(), this.h();
    },
    l(g) {
      e = Yt(g, "DIV", {
        class: !0,
        role: !0,
        "aria-label": !0
      });
      var b = ze(e);
      t = Yt(b, "LABEL", {});
      var O = ze(t);
      i = Yt(O, "DIV", { class: !0 });
      var P = ze(i);
      v && v.l(P), l = Mn(P), o = Yt(P, "TEXTAREA", {
        "data-testid": !0,
        class: !0,
        dir: !0,
        placeholder: !0,
        rows: !0,
        style: !0
      }), ze(o).forEach(ue), f = Mn(P), T && T.l(P), _ = Mn(P), k && k.l(P), d = Mn(P), w && w.l(P), P.forEach(ue), O.forEach(ue), b.forEach(ue), this.h();
    },
    h() {
      N(o, "data-testid", "textbox"), N(o, "class", "scroll-hide svelte-16q8wod"), N(o, "dir", a = /*rtl*/
      n[11] ? "rtl" : "ltr"), N(
        o,
        "placeholder",
        /*placeholder*/
        n[4]
      ), o.disabled = /*disabled*/
      n[1], N(
        o,
        "rows",
        /*lines*/
        n[3]
      ), o.autofocus = /*autofocus*/
      n[12], N(o, "style", s = `${/*stop_audio_btn*/
      n[21] ? "display: none; " : ""}${/*text_align*/
      n[13] ? "text-align: " + /*text_align*/
      n[13] + "; " : ""}flex-grow: 1;`), dt(o, "no-label", !/*show_label*/
      n[5]), N(i, "class", "input-container svelte-16q8wod"), dt(
        t,
        "container",
        /*container*/
        n[6]
      ), N(e, "class", "full-container svelte-16q8wod"), N(e, "role", "group"), N(e, "aria-label", "Multimedia input field"), dt(
        e,
        "dragging",
        /*dragging*/
        n[2]
      );
    },
    m(g, b) {
      Mt(g, e, b), We(e, t), We(t, i), v && v.m(i, null), We(i, l), We(i, o), Rl(
        o,
        /*value*/
        n[0].text
      ), n[71](o), We(i, f), T && T.m(i, null), We(i, _), k && k.m(i, null), We(i, d), w && w.m(i, null), n[75](e), c = !0, /*autofocus*/
      n[12] && o.focus(), u || (h = [
        os(r = yr.call(null, o, {
          text: (
            /*value*/
            n[0].text
          ),
          lines: (
            /*lines*/
            n[3]
          ),
          max_lines: (
            /*max_lines*/
            n[7]
          )
        })),
        Fe(
          o,
          "input",
          /*textarea_input_handler*/
          n[70]
        ),
        Fe(
          o,
          "keypress",
          /*handle_keypress*/
          n[43]
        ),
        Fe(
          o,
          "blur",
          /*blur_handler*/
          n[63]
        ),
        Fe(
          o,
          "select",
          /*handle_select*/
          n[42]
        ),
        Fe(
          o,
          "focus",
          /*focus_handler*/
          n[64]
        ),
        Fe(
          o,
          "scroll",
          /*handle_scroll*/
          n[44]
        ),
        Fe(
          o,
          "paste",
          /*handle_paste*/
          n[49]
        ),
        Fe(
          e,
          "dragenter",
          /*handle_dragenter*/
          n[50]
        ),
        Fe(
          e,
          "dragleave",
          /*handle_dragleave*/
          n[51]
        ),
        Fe(e, "dragover", fs(
          /*dragover_handler*/
          n[62]
        )),
        Fe(
          e,
          "drop",
          /*handle_drop*/
          n[52]
        )
      ], u = !0);
    },
    p(g, b) {
      /*upload_btn*/
      g[8] ? v ? (v.p(g, b), b[0] & /*upload_btn*/
      256 && mt(v, 1)) : (v = Pl(g), v.c(), mt(v, 1), v.m(i, l)) : v && (Vi(), Nt(v, 1, 1, () => {
        v = null;
      }), Wi()), (!c || b[0] & /*rtl*/
      2048 && a !== (a = /*rtl*/
      g[11] ? "rtl" : "ltr")) && N(o, "dir", a), (!c || b[0] & /*placeholder*/
      16) && N(
        o,
        "placeholder",
        /*placeholder*/
        g[4]
      ), (!c || b[0] & /*disabled*/
      2) && (o.disabled = /*disabled*/
      g[1]), (!c || b[0] & /*lines*/
      8) && N(
        o,
        "rows",
        /*lines*/
        g[3]
      ), (!c || b[0] & /*autofocus*/
      4096) && (o.autofocus = /*autofocus*/
      g[12]), (!c || b[0] & /*stop_audio_btn, text_align*/
      2105344 && s !== (s = `${/*stop_audio_btn*/
      g[21] ? "display: none; " : ""}${/*text_align*/
      g[13] ? "text-align: " + /*text_align*/
      g[13] + "; " : ""}flex-grow: 1;`)) && N(o, "style", s), r && ss(r.update) && b[0] & /*value, lines, max_lines*/
      137 && r.update.call(null, {
        text: (
          /*value*/
          g[0].text
        ),
        lines: (
          /*lines*/
          g[3]
        ),
        max_lines: (
          /*max_lines*/
          g[7]
        )
      }), b[0] & /*value*/
      1 && Rl(
        o,
        /*value*/
        g[0].text
      ), (!c || b[0] & /*show_label*/
      32) && dt(o, "no-label", !/*show_label*/
      g[5]), /*use_audio_video_recording*/
      g[33] ? T ? (T.p(g, b), b[1] & /*use_audio_video_recording*/
      4 && mt(T, 1)) : (T = Fl(g), T.c(), mt(T, 1), T.m(i, _)) : T && (Vi(), Nt(T, 1, 1, () => {
        T = null;
      }), Wi()), /*submit_btn*/
      g[9] ? k ? k.p(g, b) : (k = Ul(g), k.c(), k.m(i, d)) : k && (k.d(1), k = null), /*stop_btn*/
      g[10] ? w ? w.p(g, b) : (w = zl(g), w.c(), w.m(i, null)) : w && (w.d(1), w = null), (!c || b[0] & /*container*/
      64) && dt(
        t,
        "container",
        /*container*/
        g[6]
      ), (!c || b[0] & /*dragging*/
      4) && dt(
        e,
        "dragging",
        /*dragging*/
        g[2]
      );
    },
    i(g) {
      c || (mt(v), mt(T), c = !0);
    },
    o(g) {
      Nt(v), Nt(T), c = !1;
    },
    d(g) {
      g && ue(e), v && v.d(), n[71](null), T && T.d(), k && k.d(), w && w.d(), n[75](null), u = !1, us(h);
    }
  };
}
function ys(n, e, t) {
  var i = this && this.__awaiter || function(p, te, ge, $) {
    function st(Lt) {
      return Lt instanceof ge ? Lt : new ge(function(Ut) {
        Ut(Lt);
      });
    }
    return new (ge || (ge = Promise))(function(Lt, Ut) {
      function Yn(ft) {
        try {
          qe($.next(ft));
        } catch (an) {
          Ut(an);
        }
      }
      function Xn(ft) {
        try {
          qe($.throw(ft));
        } catch (an) {
          Ut(an);
        }
      }
      function qe(ft) {
        ft.done ? Lt(ft.value) : st(ft.value).then(Yn, Xn);
      }
      qe(($ = $.apply(p, te || [])).next());
    });
  };
  let { value: l = {
    text: "",
    files: [],
    audio: "__webrtc_value__"
  } } = e, { value_is_output: o = !1 } = e, { lines: a = 1 } = e, { placeholder: s = "Type here..." } = e, { disabled: r = !1 } = e, { interactive: f } = e, { loading_message: _ } = e, { show_label: d = !0 } = e, { container: c = !0 } = e, { max_lines: u } = e, { upload_btn: h = null } = e, { submit_btn: v = null } = e, { stop_btn: T = null } = e, { rtl: k = !1 } = e, { autofocus: w = !1 } = e, { text_align: g = void 0 } = e, { autoscroll: b = !0 } = e, { root: O } = e, { file_types: P = null } = e, { max_file_size: U = null } = e, { upload: j } = e, { stream_handler: F } = e, { file_count: L = "multiple" } = e, { audio_btn: J = !1 } = e, { stop_audio_btn: Y = !1 } = e, { gradio: ne } = e, { rtc_configuration: B } = e, { time_limit: ie = null } = e, { modality: se = "audio" } = e, { mode: Oe = "send-receive" } = e, { rtp_params: de = {} } = e, { track_constraints: be = {} } = e, { on_change_cb: Le } = e, { server: K } = e, ve, X, le, S, Te = 0, pe = !1, { dragging: D = !1 } = e, Z = !1, ee = l.text, y, M = !1, H = !1, q, x, ce, _e, me, Ae;
  navigator.language.startsWith("fr") ? (x = "Ajouter un fichier", ce = "Poser une question", _e = "Arrêter", me = "Activer Neo audio", Ae = "Arreter Neo audio") : (x = "Add a file", ce = "Ask a question", _e = "Stop", me = "Launch Neo audio", Ae = "Stop Neo audio");
  const fe = gs();
  ms(() => {
    S = le && le.offsetHeight + le.scrollTop > le.scrollHeight - 100;
  });
  const Re = () => {
    S && b && !pe && le.scrollTo(0, le.scrollHeight);
  };
  function vt() {
    return i(this, void 0, void 0, function* () {
      fe("change", l), o || fe("input");
    });
  }
  hs(() => {
    w && le !== null && le.focus(), S && b && Re(), t(55, o = !1);
  });
  function Pt(p) {
    const te = p.target, ge = te.value, $ = [te.selectionStart, te.selectionEnd];
    fe("select", { value: ge.substring(...$), index: $ });
  }
  function E(p) {
    return i(this, void 0, void 0, function* () {
      yield Ml(), (p.key === "Enter" && p.shiftKey && a > 1 || p.key === "Enter" && !p.shiftKey && a === 1 && u >= 1) && (p.preventDefault(), fe("submit"));
    });
  }
  function Tt(p) {
    const te = p.target, ge = te.scrollTop;
    ge < Te && (pe = !0), Te = ge;
    const $ = te.scrollHeight - te.clientHeight;
    ge >= $ && (pe = !1);
  }
  function At(p) {
    return i(this, arguments, void 0, function* ({ detail: te }) {
      if (vt(), Array.isArray(te)) {
        for (let ge of te)
          l.files.push(ge);
        t(0, l), t(32, Z), t(61, M), t(57, _), t(60, y);
      } else
        l.files.push(te), t(0, l), t(32, Z), t(61, M), t(57, _), t(60, y);
      yield Ml(), fe("change", l), fe("upload", te);
    });
  }
  function Hn() {
    X && (t(35, X.value = "", X), X.click());
  }
  function Wn() {
    fe("stop");
  }
  function Vn() {
    fe("submit");
  }
  function yn(p) {
    if (!p.clipboardData) return;
    const te = p.clipboardData.items;
    for (let ge in te) {
      const $ = te[ge];
      if ($.type.includes("text/plain"))
        break;
      if ($.kind === "file" && $.type.includes("image")) {
        const st = $.getAsFile();
        st && ve.load_files([st]);
      }
    }
  }
  function Gn(p) {
    p.preventDefault(), t(2, D = !0);
  }
  function tn(p) {
    p.preventDefault();
    const te = q.getBoundingClientRect(), { clientX: ge, clientY: $ } = p;
    (ge <= te.left || ge >= te.right || $ <= te.top || $ >= te.bottom) && t(2, D = !1);
  }
  function nn(p) {
    p.preventDefault(), t(2, D = !1), p.dataTransfer && p.dataTransfer.files && ve.load_files(Array.from(p.dataTransfer.files));
  }
  function $e() {
    fe("start_recording");
  }
  function St() {
    fe("stop_recording");
  }
  function En(p) {
    xn.call(this, n, p);
  }
  function Tn(p) {
    xn.call(this, n, p);
  }
  function mi(p) {
    xn.call(this, n, p);
  }
  function ln(p) {
    Qt[p ? "unshift" : "push"](() => {
      ve = p, t(34, ve);
    });
  }
  function on(p) {
    D = p, t(2, D);
  }
  function hi(p) {
    Z = p, t(32, Z);
  }
  function Ft(p) {
    X = p, t(35, X);
  }
  function gi(p) {
    xn.call(this, n, p);
  }
  function bi() {
    l.text = this.value, t(0, l), t(32, Z), t(61, M), t(57, _), t(60, y);
  }
  function he(p) {
    Qt[p ? "unshift" : "push"](() => {
      le = p, t(31, le);
    });
  }
  function Dt(p) {
    n.$$.not_equal(l.audio, p) && (l.audio = p, t(0, l), t(32, Z), t(61, M), t(57, _), t(60, y));
  }
  const pi = () => ne.dispatch("tick"), jn = ({ detail: p }) => ne.dispatch("error", p);
  function An(p) {
    Qt[p ? "unshift" : "push"](() => {
      q = p, t(36, q);
    });
  }
  return n.$$set = (p) => {
    "value" in p && t(0, l = p.value), "value_is_output" in p && t(55, o = p.value_is_output), "lines" in p && t(3, a = p.lines), "placeholder" in p && t(4, s = p.placeholder), "disabled" in p && t(1, r = p.disabled), "interactive" in p && t(56, f = p.interactive), "loading_message" in p && t(57, _ = p.loading_message), "show_label" in p && t(5, d = p.show_label), "container" in p && t(6, c = p.container), "max_lines" in p && t(7, u = p.max_lines), "upload_btn" in p && t(8, h = p.upload_btn), "submit_btn" in p && t(9, v = p.submit_btn), "stop_btn" in p && t(10, T = p.stop_btn), "rtl" in p && t(11, k = p.rtl), "autofocus" in p && t(12, w = p.autofocus), "text_align" in p && t(13, g = p.text_align), "autoscroll" in p && t(58, b = p.autoscroll), "root" in p && t(14, O = p.root), "file_types" in p && t(15, P = p.file_types), "max_file_size" in p && t(16, U = p.max_file_size), "upload" in p && t(17, j = p.upload), "stream_handler" in p && t(18, F = p.stream_handler), "file_count" in p && t(19, L = p.file_count), "audio_btn" in p && t(20, J = p.audio_btn), "stop_audio_btn" in p && t(21, Y = p.stop_audio_btn), "gradio" in p && t(22, ne = p.gradio), "rtc_configuration" in p && t(23, B = p.rtc_configuration), "time_limit" in p && t(24, ie = p.time_limit), "modality" in p && t(25, se = p.modality), "mode" in p && t(26, Oe = p.mode), "rtp_params" in p && t(27, de = p.rtp_params), "track_constraints" in p && t(28, be = p.track_constraints), "on_change_cb" in p && t(29, Le = p.on_change_cb), "server" in p && t(30, K = p.server), "dragging" in p && t(2, D = p.dragging);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*dragging*/
    4 && fe("drag", D), n.$$.dirty[0] & /*audio_btn*/
    1048576 | n.$$.dirty[1] & /*use_audio_video_recording*/
    4 && J && !H && t(33, H = J), n.$$.dirty[0] & /*value*/
    1 && l === null && t(0, l = { text: "", files: [], audio: null }), n.$$.dirty[0] & /*value*/
    1 | n.$$.dirty[1] & /*uploading, retrieve_saved_message, loading_message, saved_message*/
    1677721602 && (Z && !M ? (t(60, y = l.text), t(61, M = !0), t(0, l.text = _, l), console.log("value.text uploading", l.text)) : !Z && M && (t(0, l.text = y, l), t(61, M = !1), console.log("value.text end of uploading", l.text))), n.$$.dirty[0] & /*value*/
    1 | n.$$.dirty[1] & /*oldValue, uploading, retrieve_saved_message*/
    1342177282 && ee !== l.text && !Z && !M && (t(59, ee = l.text), fe("change", l)), n.$$.dirty[1] & /*uploading*/
    2 && Z && console.log("uploading"), n.$$.dirty[1] & /*interactive, uploading*/
    33554434 && t(1, r = !f || Z), n.$$.dirty[0] & /*disabled*/
    2 && r && console.log("disabled"), n.$$.dirty[0] & /*value, lines, max_lines*/
    137 | n.$$.dirty[1] & /*el, uploading*/
    3 && le && a !== u && Bi(le, a, u, Z);
  }, [
    l,
    r,
    D,
    a,
    s,
    d,
    c,
    u,
    h,
    v,
    T,
    k,
    w,
    g,
    O,
    P,
    U,
    j,
    F,
    L,
    J,
    Y,
    ne,
    B,
    ie,
    se,
    Oe,
    de,
    be,
    Le,
    K,
    le,
    Z,
    H,
    ve,
    X,
    q,
    x,
    ce,
    _e,
    me,
    Ae,
    Pt,
    E,
    Tt,
    At,
    Hn,
    Wn,
    Vn,
    yn,
    Gn,
    tn,
    nn,
    $e,
    St,
    o,
    f,
    _,
    b,
    ee,
    y,
    M,
    En,
    Tn,
    mi,
    ln,
    on,
    hi,
    Ft,
    gi,
    bi,
    he,
    Dt,
    pi,
    jn,
    An
  ];
}
class Es extends ls {
  constructor(e) {
    super(), rs(
      this,
      e,
      ys,
      ks,
      cs,
      {
        value: 0,
        value_is_output: 55,
        lines: 3,
        placeholder: 4,
        disabled: 1,
        interactive: 56,
        loading_message: 57,
        show_label: 5,
        container: 6,
        max_lines: 7,
        upload_btn: 8,
        submit_btn: 9,
        stop_btn: 10,
        rtl: 11,
        autofocus: 12,
        text_align: 13,
        autoscroll: 58,
        root: 14,
        file_types: 15,
        max_file_size: 16,
        upload: 17,
        stream_handler: 18,
        file_count: 19,
        audio_btn: 20,
        stop_audio_btn: 21,
        gradio: 22,
        rtc_configuration: 23,
        time_limit: 24,
        modality: 25,
        mode: 26,
        rtp_params: 27,
        track_constraints: 28,
        on_change_cb: 29,
        server: 30,
        dragging: 2
      },
      null,
      [-1, -1, -1]
    );
  }
}
function dn(n) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; n > 1e3 && t < e.length - 1; )
    n /= 1e3, t++;
  let i = e[t];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + i;
}
function oi() {
}
function Ts(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
const zo = typeof window < "u";
let ql = zo ? () => window.performance.now() : () => Date.now(), qo = zo ? (n) => requestAnimationFrame(n) : oi;
const hn = /* @__PURE__ */ new Set();
function Bo(n) {
  hn.forEach((e) => {
    e.c(n) || (hn.delete(e), e.f());
  }), hn.size !== 0 && qo(Bo);
}
function As(n) {
  let e;
  return hn.size === 0 && qo(Bo), {
    promise: new Promise((t) => {
      hn.add(e = { c: n, f: t });
    }),
    abort() {
      hn.delete(e);
    }
  };
}
const sn = [];
function Ss(n, e = oi) {
  let t;
  const i = /* @__PURE__ */ new Set();
  function l(s) {
    if (Ts(n, s) && (n = s, t)) {
      const r = !sn.length;
      for (const f of i)
        f[1](), sn.push(f, n);
      if (r) {
        for (let f = 0; f < sn.length; f += 2)
          sn[f][0](sn[f + 1]);
        sn.length = 0;
      }
    }
  }
  function o(s) {
    l(s(n));
  }
  function a(s, r = oi) {
    const f = [s, r];
    return i.add(f), i.size === 1 && (t = e(l, o) || oi), s(n), () => {
      i.delete(f), i.size === 0 && t && (t(), t = null);
    };
  }
  return { set: l, update: o, subscribe: a };
}
function Bl(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function Gi(n, e, t, i) {
  if (typeof t == "number" || Bl(t)) {
    const l = i - t, o = (t - e) / (n.dt || 1 / 60), a = n.opts.stiffness * l, s = n.opts.damping * o, r = (a - s) * n.inv_mass, f = (o + r) * n.dt;
    return Math.abs(f) < n.opts.precision && Math.abs(l) < n.opts.precision ? i : (n.settled = !1, Bl(t) ? new Date(t.getTime() + f) : t + f);
  } else {
    if (Array.isArray(t))
      return t.map(
        (l, o) => Gi(n, e[o], t[o], i[o])
      );
    if (typeof t == "object") {
      const l = {};
      for (const o in t)
        l[o] = Gi(n, e[o], t[o], i[o]);
      return l;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function Hl(n, e = {}) {
  const t = Ss(n), { stiffness: i = 0.15, damping: l = 0.8, precision: o = 0.01 } = e;
  let a, s, r, f = n, _ = n, d = 1, c = 0, u = !1;
  function h(T, k = {}) {
    _ = T;
    const w = r = {};
    return n == null || k.hard || v.stiffness >= 1 && v.damping >= 1 ? (u = !0, a = ql(), f = T, t.set(n = _), Promise.resolve()) : (k.soft && (c = 1 / ((k.soft === !0 ? 0.5 : +k.soft) * 60), d = 0), s || (a = ql(), u = !1, s = As((g) => {
      if (u)
        return u = !1, s = null, !1;
      d = Math.min(d + c, 1);
      const b = {
        inv_mass: d,
        opts: v,
        settled: !0,
        dt: (g - a) * 60 / 1e3
      }, O = Gi(b, f, n, _);
      return a = g, f = n, t.set(n = O), b.settled && (s = null), !b.settled;
    })), new Promise((g) => {
      s.promise.then(() => {
        w === r && g();
      });
    }));
  }
  const v = {
    set: h,
    update: (T, k) => h(T(_, n), k),
    subscribe: t.subscribe,
    stiffness: i,
    damping: l,
    precision: o
  };
  return v;
}
const {
  SvelteComponent: Ds,
  append_hydration: tt,
  attr: Q,
  children: je,
  claim_element: Ls,
  claim_svg_element: nt,
  component_subscribe: Wl,
  detach: Be,
  element: Cs,
  init: Is,
  insert_hydration: Ns,
  noop: Vl,
  safe_not_equal: Os,
  set_style: $n,
  svg_element: it,
  toggle_class: Gl
} = window.__gradio__svelte__internal, { onMount: Rs } = window.__gradio__svelte__internal;
function Ms(n) {
  let e, t, i, l, o, a, s, r, f, _, d, c;
  return {
    c() {
      e = Cs("div"), t = it("svg"), i = it("g"), l = it("path"), o = it("path"), a = it("path"), s = it("path"), r = it("g"), f = it("path"), _ = it("path"), d = it("path"), c = it("path"), this.h();
    },
    l(u) {
      e = Ls(u, "DIV", { class: !0 });
      var h = je(e);
      t = nt(h, "svg", {
        viewBox: !0,
        fill: !0,
        xmlns: !0,
        class: !0
      });
      var v = je(t);
      i = nt(v, "g", { style: !0 });
      var T = je(i);
      l = nt(T, "path", {
        d: !0,
        fill: !0,
        "fill-opacity": !0,
        class: !0
      }), je(l).forEach(Be), o = nt(T, "path", { d: !0, fill: !0, class: !0 }), je(o).forEach(Be), a = nt(T, "path", {
        d: !0,
        fill: !0,
        "fill-opacity": !0,
        class: !0
      }), je(a).forEach(Be), s = nt(T, "path", { d: !0, fill: !0, class: !0 }), je(s).forEach(Be), T.forEach(Be), r = nt(v, "g", { style: !0 });
      var k = je(r);
      f = nt(k, "path", {
        d: !0,
        fill: !0,
        "fill-opacity": !0,
        class: !0
      }), je(f).forEach(Be), _ = nt(k, "path", { d: !0, fill: !0, class: !0 }), je(_).forEach(Be), d = nt(k, "path", {
        d: !0,
        fill: !0,
        "fill-opacity": !0,
        class: !0
      }), je(d).forEach(Be), c = nt(k, "path", { d: !0, fill: !0, class: !0 }), je(c).forEach(Be), k.forEach(Be), v.forEach(Be), h.forEach(Be), this.h();
    },
    h() {
      Q(l, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), Q(l, "fill", "#FF7C00"), Q(l, "fill-opacity", "0.4"), Q(l, "class", "svelte-43sxxs"), Q(o, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), Q(o, "fill", "#FF7C00"), Q(o, "class", "svelte-43sxxs"), Q(a, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), Q(a, "fill", "#FF7C00"), Q(a, "fill-opacity", "0.4"), Q(a, "class", "svelte-43sxxs"), Q(s, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), Q(s, "fill", "#FF7C00"), Q(s, "class", "svelte-43sxxs"), $n(i, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), Q(f, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), Q(f, "fill", "#FF7C00"), Q(f, "fill-opacity", "0.4"), Q(f, "class", "svelte-43sxxs"), Q(_, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), Q(_, "fill", "#FF7C00"), Q(_, "class", "svelte-43sxxs"), Q(d, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), Q(d, "fill", "#FF7C00"), Q(d, "fill-opacity", "0.4"), Q(d, "class", "svelte-43sxxs"), Q(c, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), Q(c, "fill", "#FF7C00"), Q(c, "class", "svelte-43sxxs"), $n(r, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), Q(t, "viewBox", "-1200 -1200 3000 3000"), Q(t, "fill", "none"), Q(t, "xmlns", "http://www.w3.org/2000/svg"), Q(t, "class", "svelte-43sxxs"), Q(e, "class", "svelte-43sxxs"), Gl(
        e,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(u, h) {
      Ns(u, e, h), tt(e, t), tt(t, i), tt(i, l), tt(i, o), tt(i, a), tt(i, s), tt(t, r), tt(r, f), tt(r, _), tt(r, d), tt(r, c);
    },
    p(u, [h]) {
      h & /*$top*/
      2 && $n(i, "transform", "translate(" + /*$top*/
      u[1][0] + "px, " + /*$top*/
      u[1][1] + "px)"), h & /*$bottom*/
      4 && $n(r, "transform", "translate(" + /*$bottom*/
      u[2][0] + "px, " + /*$bottom*/
      u[2][1] + "px)"), h & /*margin*/
      1 && Gl(
        e,
        "margin",
        /*margin*/
        u[0]
      );
    },
    i: Vl,
    o: Vl,
    d(u) {
      u && Be(e);
    }
  };
}
function Ps(n, e, t) {
  let i, l;
  var o = this && this.__awaiter || function(u, h, v, T) {
    function k(w) {
      return w instanceof v ? w : new v(function(g) {
        g(w);
      });
    }
    return new (v || (v = Promise))(function(w, g) {
      function b(U) {
        try {
          P(T.next(U));
        } catch (j) {
          g(j);
        }
      }
      function O(U) {
        try {
          P(T.throw(U));
        } catch (j) {
          g(j);
        }
      }
      function P(U) {
        U.done ? w(U.value) : k(U.value).then(b, O);
      }
      P((T = T.apply(u, h || [])).next());
    });
  };
  let { margin: a = !0 } = e;
  const s = Hl([0, 0]);
  Wl(n, s, (u) => t(1, i = u));
  const r = Hl([0, 0]);
  Wl(n, r, (u) => t(2, l = u));
  let f;
  function _() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([s.set([125, 140]), r.set([-125, -140])]), yield Promise.all([s.set([-125, 140]), r.set([125, -140])]), yield Promise.all([s.set([-125, 0]), r.set([125, -0])]), yield Promise.all([s.set([125, 0]), r.set([-125, 0])]);
    });
  }
  function d() {
    return o(this, void 0, void 0, function* () {
      yield _(), f || d();
    });
  }
  function c() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([s.set([125, 0]), r.set([-125, 0])]), d();
    });
  }
  return Rs(() => (c(), () => f = !0)), n.$$set = (u) => {
    "margin" in u && t(0, a = u.margin);
  }, [a, i, l, s, r];
}
class Fs extends Ds {
  constructor(e) {
    super(), Is(this, e, Ps, Ms, Os, { margin: 0 });
  }
}
const {
  SvelteComponent: Us,
  append_hydration: Zt,
  attr: rt,
  binding_callbacks: jl,
  check_outros: ji,
  children: gt,
  claim_component: Ho,
  claim_element: bt,
  claim_space: Xe,
  claim_text: ae,
  create_component: Wo,
  create_slot: Vo,
  destroy_component: Go,
  destroy_each: jo,
  detach: R,
  element: pt,
  empty: Je,
  ensure_array_like: _i,
  get_all_dirty_from_scope: Yo,
  get_slot_changes: Xo,
  group_outros: Yi,
  init: zs,
  insert_hydration: z,
  mount_component: Zo,
  noop: Xi,
  safe_not_equal: qs,
  set_data: Qe,
  set_style: Ot,
  space: Ze,
  text: re,
  toggle_class: Ye,
  transition_in: at,
  transition_out: wt,
  update_slot_base: Ko
} = window.__gradio__svelte__internal, { tick: Bs } = window.__gradio__svelte__internal, { onDestroy: Hs } = window.__gradio__svelte__internal, { createEventDispatcher: Ws } = window.__gradio__svelte__internal, Vs = (n) => ({}), Yl = (n) => ({}), Gs = (n) => ({}), Xl = (n) => ({});
function Zl(n, e, t) {
  const i = n.slice();
  return i[41] = e[t], i[43] = t, i;
}
function Kl(n, e, t) {
  const i = n.slice();
  return i[41] = e[t], i;
}
function js(n) {
  let e, t, i, l, o = (
    /*i18n*/
    n[1]("common.error") + ""
  ), a, s, r;
  t = new dr({
    props: {
      Icon: wr,
      label: (
        /*i18n*/
        n[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    n[32]
  );
  const f = (
    /*#slots*/
    n[30].error
  ), _ = Vo(
    f,
    n,
    /*$$scope*/
    n[29],
    Yl
  );
  return {
    c() {
      e = pt("div"), Wo(t.$$.fragment), i = Ze(), l = pt("span"), a = re(o), s = Ze(), _ && _.c(), this.h();
    },
    l(d) {
      e = bt(d, "DIV", { class: !0 });
      var c = gt(e);
      Ho(t.$$.fragment, c), c.forEach(R), i = Xe(d), l = bt(d, "SPAN", { class: !0 });
      var u = gt(l);
      a = ae(u, o), u.forEach(R), s = Xe(d), _ && _.l(d), this.h();
    },
    h() {
      rt(e, "class", "clear-status svelte-17v219f"), rt(l, "class", "error svelte-17v219f");
    },
    m(d, c) {
      z(d, e, c), Zo(t, e, null), z(d, i, c), z(d, l, c), Zt(l, a), z(d, s, c), _ && _.m(d, c), r = !0;
    },
    p(d, c) {
      const u = {};
      c[0] & /*i18n*/
      2 && (u.label = /*i18n*/
      d[1]("common.clear")), t.$set(u), (!r || c[0] & /*i18n*/
      2) && o !== (o = /*i18n*/
      d[1]("common.error") + "") && Qe(a, o), _ && _.p && (!r || c[0] & /*$$scope*/
      536870912) && Ko(
        _,
        f,
        d,
        /*$$scope*/
        d[29],
        r ? Xo(
          f,
          /*$$scope*/
          d[29],
          c,
          Vs
        ) : Yo(
          /*$$scope*/
          d[29]
        ),
        Yl
      );
    },
    i(d) {
      r || (at(t.$$.fragment, d), at(_, d), r = !0);
    },
    o(d) {
      wt(t.$$.fragment, d), wt(_, d), r = !1;
    },
    d(d) {
      d && (R(e), R(i), R(l), R(s)), Go(t), _ && _.d(d);
    }
  };
}
function Ys(n) {
  let e, t, i, l, o, a, s, r, f, _ = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && Jl(n)
  );
  function d(g, b) {
    if (
      /*progress*/
      g[7]
    ) return Ks;
    if (
      /*queue_position*/
      g[2] !== null && /*queue_size*/
      g[3] !== void 0 && /*queue_position*/
      g[2] >= 0
    ) return Zs;
    if (
      /*queue_position*/
      g[2] === 0
    ) return Xs;
  }
  let c = d(n), u = c && c(n), h = (
    /*timer*/
    n[5] && $l(n)
  );
  const v = [$s, xs], T = [];
  function k(g, b) {
    return (
      /*last_progress_level*/
      g[15] != null ? 0 : (
        /*show_progress*/
        g[6] === "full" ? 1 : -1
      )
    );
  }
  ~(o = k(n)) && (a = T[o] = v[o](n));
  let w = !/*timer*/
  n[5] && ao(n);
  return {
    c() {
      _ && _.c(), e = Ze(), t = pt("div"), u && u.c(), i = Ze(), h && h.c(), l = Ze(), a && a.c(), s = Ze(), w && w.c(), r = Je(), this.h();
    },
    l(g) {
      _ && _.l(g), e = Xe(g), t = bt(g, "DIV", { class: !0 });
      var b = gt(t);
      u && u.l(b), i = Xe(b), h && h.l(b), b.forEach(R), l = Xe(g), a && a.l(g), s = Xe(g), w && w.l(g), r = Je(), this.h();
    },
    h() {
      rt(t, "class", "progress-text svelte-17v219f"), Ye(
        t,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), Ye(
        t,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(g, b) {
      _ && _.m(g, b), z(g, e, b), z(g, t, b), u && u.m(t, null), Zt(t, i), h && h.m(t, null), z(g, l, b), ~o && T[o].m(g, b), z(g, s, b), w && w.m(g, b), z(g, r, b), f = !0;
    },
    p(g, b) {
      /*variant*/
      g[8] === "default" && /*show_eta_bar*/
      g[18] && /*show_progress*/
      g[6] === "full" ? _ ? _.p(g, b) : (_ = Jl(g), _.c(), _.m(e.parentNode, e)) : _ && (_.d(1), _ = null), c === (c = d(g)) && u ? u.p(g, b) : (u && u.d(1), u = c && c(g), u && (u.c(), u.m(t, i))), /*timer*/
      g[5] ? h ? h.p(g, b) : (h = $l(g), h.c(), h.m(t, null)) : h && (h.d(1), h = null), (!f || b[0] & /*variant*/
      256) && Ye(
        t,
        "meta-text-center",
        /*variant*/
        g[8] === "center"
      ), (!f || b[0] & /*variant*/
      256) && Ye(
        t,
        "meta-text",
        /*variant*/
        g[8] === "default"
      );
      let O = o;
      o = k(g), o === O ? ~o && T[o].p(g, b) : (a && (Yi(), wt(T[O], 1, 1, () => {
        T[O] = null;
      }), ji()), ~o ? (a = T[o], a ? a.p(g, b) : (a = T[o] = v[o](g), a.c()), at(a, 1), a.m(s.parentNode, s)) : a = null), /*timer*/
      g[5] ? w && (Yi(), wt(w, 1, 1, () => {
        w = null;
      }), ji()) : w ? (w.p(g, b), b[0] & /*timer*/
      32 && at(w, 1)) : (w = ao(g), w.c(), at(w, 1), w.m(r.parentNode, r));
    },
    i(g) {
      f || (at(a), at(w), f = !0);
    },
    o(g) {
      wt(a), wt(w), f = !1;
    },
    d(g) {
      g && (R(e), R(t), R(l), R(s), R(r)), _ && _.d(g), u && u.d(), h && h.d(), ~o && T[o].d(g), w && w.d(g);
    }
  };
}
function Jl(n) {
  let e, t = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = pt("div"), this.h();
    },
    l(i) {
      e = bt(i, "DIV", { class: !0 }), gt(e).forEach(R), this.h();
    },
    h() {
      rt(e, "class", "eta-bar svelte-17v219f"), Ot(e, "transform", t);
    },
    m(i, l) {
      z(i, e, l);
    },
    p(i, l) {
      l[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (i[17] || 0) * 100 - 100}%)`) && Ot(e, "transform", t);
    },
    d(i) {
      i && R(e);
    }
  };
}
function Xs(n) {
  let e;
  return {
    c() {
      e = re("processing |");
    },
    l(t) {
      e = ae(t, "processing |");
    },
    m(t, i) {
      z(t, e, i);
    },
    p: Xi,
    d(t) {
      t && R(e);
    }
  };
}
function Zs(n) {
  let e, t = (
    /*queue_position*/
    n[2] + 1 + ""
  ), i, l, o, a;
  return {
    c() {
      e = re("queue: "), i = re(t), l = re("/"), o = re(
        /*queue_size*/
        n[3]
      ), a = re(" |");
    },
    l(s) {
      e = ae(s, "queue: "), i = ae(s, t), l = ae(s, "/"), o = ae(
        s,
        /*queue_size*/
        n[3]
      ), a = ae(s, " |");
    },
    m(s, r) {
      z(s, e, r), z(s, i, r), z(s, l, r), z(s, o, r), z(s, a, r);
    },
    p(s, r) {
      r[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      s[2] + 1 + "") && Qe(i, t), r[0] & /*queue_size*/
      8 && Qe(
        o,
        /*queue_size*/
        s[3]
      );
    },
    d(s) {
      s && (R(e), R(i), R(l), R(o), R(a));
    }
  };
}
function Ks(n) {
  let e, t = _i(
    /*progress*/
    n[7]
  ), i = [];
  for (let l = 0; l < t.length; l += 1)
    i[l] = xl(Kl(n, t, l));
  return {
    c() {
      for (let l = 0; l < i.length; l += 1)
        i[l].c();
      e = Je();
    },
    l(l) {
      for (let o = 0; o < i.length; o += 1)
        i[o].l(l);
      e = Je();
    },
    m(l, o) {
      for (let a = 0; a < i.length; a += 1)
        i[a] && i[a].m(l, o);
      z(l, e, o);
    },
    p(l, o) {
      if (o[0] & /*progress*/
      128) {
        t = _i(
          /*progress*/
          l[7]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const s = Kl(l, t, a);
          i[a] ? i[a].p(s, o) : (i[a] = xl(s), i[a].c(), i[a].m(e.parentNode, e));
        }
        for (; a < i.length; a += 1)
          i[a].d(1);
        i.length = t.length;
      }
    },
    d(l) {
      l && R(e), jo(i, l);
    }
  };
}
function Ql(n) {
  let e, t = (
    /*p*/
    n[41].unit + ""
  ), i, l, o = " ", a;
  function s(_, d) {
    return (
      /*p*/
      _[41].length != null ? Qs : Js
    );
  }
  let r = s(n), f = r(n);
  return {
    c() {
      f.c(), e = Ze(), i = re(t), l = re(" | "), a = re(o);
    },
    l(_) {
      f.l(_), e = Xe(_), i = ae(_, t), l = ae(_, " | "), a = ae(_, o);
    },
    m(_, d) {
      f.m(_, d), z(_, e, d), z(_, i, d), z(_, l, d), z(_, a, d);
    },
    p(_, d) {
      r === (r = s(_)) && f ? f.p(_, d) : (f.d(1), f = r(_), f && (f.c(), f.m(e.parentNode, e))), d[0] & /*progress*/
      128 && t !== (t = /*p*/
      _[41].unit + "") && Qe(i, t);
    },
    d(_) {
      _ && (R(e), R(i), R(l), R(a)), f.d(_);
    }
  };
}
function Js(n) {
  let e = dn(
    /*p*/
    n[41].index || 0
  ) + "", t;
  return {
    c() {
      t = re(e);
    },
    l(i) {
      t = ae(i, e);
    },
    m(i, l) {
      z(i, t, l);
    },
    p(i, l) {
      l[0] & /*progress*/
      128 && e !== (e = dn(
        /*p*/
        i[41].index || 0
      ) + "") && Qe(t, e);
    },
    d(i) {
      i && R(t);
    }
  };
}
function Qs(n) {
  let e = dn(
    /*p*/
    n[41].index || 0
  ) + "", t, i, l = dn(
    /*p*/
    n[41].length
  ) + "", o;
  return {
    c() {
      t = re(e), i = re("/"), o = re(l);
    },
    l(a) {
      t = ae(a, e), i = ae(a, "/"), o = ae(a, l);
    },
    m(a, s) {
      z(a, t, s), z(a, i, s), z(a, o, s);
    },
    p(a, s) {
      s[0] & /*progress*/
      128 && e !== (e = dn(
        /*p*/
        a[41].index || 0
      ) + "") && Qe(t, e), s[0] & /*progress*/
      128 && l !== (l = dn(
        /*p*/
        a[41].length
      ) + "") && Qe(o, l);
    },
    d(a) {
      a && (R(t), R(i), R(o));
    }
  };
}
function xl(n) {
  let e, t = (
    /*p*/
    n[41].index != null && Ql(n)
  );
  return {
    c() {
      t && t.c(), e = Je();
    },
    l(i) {
      t && t.l(i), e = Je();
    },
    m(i, l) {
      t && t.m(i, l), z(i, e, l);
    },
    p(i, l) {
      /*p*/
      i[41].index != null ? t ? t.p(i, l) : (t = Ql(i), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(i) {
      i && R(e), t && t.d(i);
    }
  };
}
function $l(n) {
  let e, t = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), i, l;
  return {
    c() {
      e = re(
        /*formatted_timer*/
        n[20]
      ), i = re(t), l = re("s");
    },
    l(o) {
      e = ae(
        o,
        /*formatted_timer*/
        n[20]
      ), i = ae(o, t), l = ae(o, "s");
    },
    m(o, a) {
      z(o, e, a), z(o, i, a), z(o, l, a);
    },
    p(o, a) {
      a[0] & /*formatted_timer*/
      1048576 && Qe(
        e,
        /*formatted_timer*/
        o[20]
      ), a[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      o[0] ? `/${/*formatted_eta*/
      o[19]}` : "") && Qe(i, t);
    },
    d(o) {
      o && (R(e), R(i), R(l));
    }
  };
}
function xs(n) {
  let e, t;
  return e = new Fs({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      Wo(e.$$.fragment);
    },
    l(i) {
      Ho(e.$$.fragment, i);
    },
    m(i, l) {
      Zo(e, i, l), t = !0;
    },
    p(i, l) {
      const o = {};
      l[0] & /*variant*/
      256 && (o.margin = /*variant*/
      i[8] === "default"), e.$set(o);
    },
    i(i) {
      t || (at(e.$$.fragment, i), t = !0);
    },
    o(i) {
      wt(e.$$.fragment, i), t = !1;
    },
    d(i) {
      Go(e, i);
    }
  };
}
function $s(n) {
  let e, t, i, l, o, a = `${/*last_progress_level*/
  n[15] * 100}%`, s = (
    /*progress*/
    n[7] != null && eo(n)
  );
  return {
    c() {
      e = pt("div"), t = pt("div"), s && s.c(), i = Ze(), l = pt("div"), o = pt("div"), this.h();
    },
    l(r) {
      e = bt(r, "DIV", { class: !0 });
      var f = gt(e);
      t = bt(f, "DIV", { class: !0 });
      var _ = gt(t);
      s && s.l(_), _.forEach(R), i = Xe(f), l = bt(f, "DIV", { class: !0 });
      var d = gt(l);
      o = bt(d, "DIV", { class: !0 }), gt(o).forEach(R), d.forEach(R), f.forEach(R), this.h();
    },
    h() {
      rt(t, "class", "progress-level-inner svelte-17v219f"), rt(o, "class", "progress-bar svelte-17v219f"), Ot(o, "width", a), rt(l, "class", "progress-bar-wrap svelte-17v219f"), rt(e, "class", "progress-level svelte-17v219f");
    },
    m(r, f) {
      z(r, e, f), Zt(e, t), s && s.m(t, null), Zt(e, i), Zt(e, l), Zt(l, o), n[31](o);
    },
    p(r, f) {
      /*progress*/
      r[7] != null ? s ? s.p(r, f) : (s = eo(r), s.c(), s.m(t, null)) : s && (s.d(1), s = null), f[0] & /*last_progress_level*/
      32768 && a !== (a = `${/*last_progress_level*/
      r[15] * 100}%`) && Ot(o, "width", a);
    },
    i: Xi,
    o: Xi,
    d(r) {
      r && R(e), s && s.d(), n[31](null);
    }
  };
}
function eo(n) {
  let e, t = _i(
    /*progress*/
    n[7]
  ), i = [];
  for (let l = 0; l < t.length; l += 1)
    i[l] = oo(Zl(n, t, l));
  return {
    c() {
      for (let l = 0; l < i.length; l += 1)
        i[l].c();
      e = Je();
    },
    l(l) {
      for (let o = 0; o < i.length; o += 1)
        i[o].l(l);
      e = Je();
    },
    m(l, o) {
      for (let a = 0; a < i.length; a += 1)
        i[a] && i[a].m(l, o);
      z(l, e, o);
    },
    p(l, o) {
      if (o[0] & /*progress_level, progress*/
      16512) {
        t = _i(
          /*progress*/
          l[7]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const s = Zl(l, t, a);
          i[a] ? i[a].p(s, o) : (i[a] = oo(s), i[a].c(), i[a].m(e.parentNode, e));
        }
        for (; a < i.length; a += 1)
          i[a].d(1);
        i.length = t.length;
      }
    },
    d(l) {
      l && R(e), jo(i, l);
    }
  };
}
function to(n) {
  let e, t, i, l, o = (
    /*i*/
    n[43] !== 0 && ef()
  ), a = (
    /*p*/
    n[41].desc != null && no(n)
  ), s = (
    /*p*/
    n[41].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[43]
    ] != null && io()
  ), r = (
    /*progress_level*/
    n[14] != null && lo(n)
  );
  return {
    c() {
      o && o.c(), e = Ze(), a && a.c(), t = Ze(), s && s.c(), i = Ze(), r && r.c(), l = Je();
    },
    l(f) {
      o && o.l(f), e = Xe(f), a && a.l(f), t = Xe(f), s && s.l(f), i = Xe(f), r && r.l(f), l = Je();
    },
    m(f, _) {
      o && o.m(f, _), z(f, e, _), a && a.m(f, _), z(f, t, _), s && s.m(f, _), z(f, i, _), r && r.m(f, _), z(f, l, _);
    },
    p(f, _) {
      /*p*/
      f[41].desc != null ? a ? a.p(f, _) : (a = no(f), a.c(), a.m(t.parentNode, t)) : a && (a.d(1), a = null), /*p*/
      f[41].desc != null && /*progress_level*/
      f[14] && /*progress_level*/
      f[14][
        /*i*/
        f[43]
      ] != null ? s || (s = io(), s.c(), s.m(i.parentNode, i)) : s && (s.d(1), s = null), /*progress_level*/
      f[14] != null ? r ? r.p(f, _) : (r = lo(f), r.c(), r.m(l.parentNode, l)) : r && (r.d(1), r = null);
    },
    d(f) {
      f && (R(e), R(t), R(i), R(l)), o && o.d(f), a && a.d(f), s && s.d(f), r && r.d(f);
    }
  };
}
function ef(n) {
  let e;
  return {
    c() {
      e = re(" /");
    },
    l(t) {
      e = ae(t, " /");
    },
    m(t, i) {
      z(t, e, i);
    },
    d(t) {
      t && R(e);
    }
  };
}
function no(n) {
  let e = (
    /*p*/
    n[41].desc + ""
  ), t;
  return {
    c() {
      t = re(e);
    },
    l(i) {
      t = ae(i, e);
    },
    m(i, l) {
      z(i, t, l);
    },
    p(i, l) {
      l[0] & /*progress*/
      128 && e !== (e = /*p*/
      i[41].desc + "") && Qe(t, e);
    },
    d(i) {
      i && R(t);
    }
  };
}
function io(n) {
  let e;
  return {
    c() {
      e = re("-");
    },
    l(t) {
      e = ae(t, "-");
    },
    m(t, i) {
      z(t, e, i);
    },
    d(t) {
      t && R(e);
    }
  };
}
function lo(n) {
  let e = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[43]
  ] || 0)).toFixed(1) + "", t, i;
  return {
    c() {
      t = re(e), i = re("%");
    },
    l(l) {
      t = ae(l, e), i = ae(l, "%");
    },
    m(l, o) {
      z(l, t, o), z(l, i, o);
    },
    p(l, o) {
      o[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (l[14][
        /*i*/
        l[43]
      ] || 0)).toFixed(1) + "") && Qe(t, e);
    },
    d(l) {
      l && (R(t), R(i));
    }
  };
}
function oo(n) {
  let e, t = (
    /*p*/
    (n[41].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[43]
    ] != null) && to(n)
  );
  return {
    c() {
      t && t.c(), e = Je();
    },
    l(i) {
      t && t.l(i), e = Je();
    },
    m(i, l) {
      t && t.m(i, l), z(i, e, l);
    },
    p(i, l) {
      /*p*/
      i[41].desc != null || /*progress_level*/
      i[14] && /*progress_level*/
      i[14][
        /*i*/
        i[43]
      ] != null ? t ? t.p(i, l) : (t = to(i), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(i) {
      i && R(e), t && t.d(i);
    }
  };
}
function ao(n) {
  let e, t, i, l;
  const o = (
    /*#slots*/
    n[30]["additional-loading-text"]
  ), a = Vo(
    o,
    n,
    /*$$scope*/
    n[29],
    Xl
  );
  return {
    c() {
      e = pt("p"), t = re(
        /*loading_text*/
        n[9]
      ), i = Ze(), a && a.c(), this.h();
    },
    l(s) {
      e = bt(s, "P", { class: !0 });
      var r = gt(e);
      t = ae(
        r,
        /*loading_text*/
        n[9]
      ), r.forEach(R), i = Xe(s), a && a.l(s), this.h();
    },
    h() {
      rt(e, "class", "loading svelte-17v219f");
    },
    m(s, r) {
      z(s, e, r), Zt(e, t), z(s, i, r), a && a.m(s, r), l = !0;
    },
    p(s, r) {
      (!l || r[0] & /*loading_text*/
      512) && Qe(
        t,
        /*loading_text*/
        s[9]
      ), a && a.p && (!l || r[0] & /*$$scope*/
      536870912) && Ko(
        a,
        o,
        s,
        /*$$scope*/
        s[29],
        l ? Xo(
          o,
          /*$$scope*/
          s[29],
          r,
          Gs
        ) : Yo(
          /*$$scope*/
          s[29]
        ),
        Xl
      );
    },
    i(s) {
      l || (at(a, s), l = !0);
    },
    o(s) {
      wt(a, s), l = !1;
    },
    d(s) {
      s && (R(e), R(i)), a && a.d(s);
    }
  };
}
function tf(n) {
  let e, t, i, l, o;
  const a = [Ys, js], s = [];
  function r(f, _) {
    return (
      /*status*/
      f[4] === "pending" ? 0 : (
        /*status*/
        f[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = r(n)) && (i = s[t] = a[t](n)), {
    c() {
      e = pt("div"), i && i.c(), this.h();
    },
    l(f) {
      e = bt(f, "DIV", { class: !0 });
      var _ = gt(e);
      i && i.l(_), _.forEach(R), this.h();
    },
    h() {
      rt(e, "class", l = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-17v219f"), Ye(e, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden" || /*status*/
      n[4] == "streaming"), Ye(
        e,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), Ye(
        e,
        "generating",
        /*status*/
        n[4] === "generating" && /*show_progress*/
        n[6] === "full"
      ), Ye(
        e,
        "border",
        /*border*/
        n[12]
      ), Ot(
        e,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), Ot(
        e,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(f, _) {
      z(f, e, _), ~t && s[t].m(e, null), n[33](e), o = !0;
    },
    p(f, _) {
      let d = t;
      t = r(f), t === d ? ~t && s[t].p(f, _) : (i && (Yi(), wt(s[d], 1, 1, () => {
        s[d] = null;
      }), ji()), ~t ? (i = s[t], i ? i.p(f, _) : (i = s[t] = a[t](f), i.c()), at(i, 1), i.m(e, null)) : i = null), (!o || _[0] & /*variant, show_progress*/
      320 && l !== (l = "wrap " + /*variant*/
      f[8] + " " + /*show_progress*/
      f[6] + " svelte-17v219f")) && rt(e, "class", l), (!o || _[0] & /*variant, show_progress, status, show_progress*/
      336) && Ye(e, "hide", !/*status*/
      f[4] || /*status*/
      f[4] === "complete" || /*show_progress*/
      f[6] === "hidden" || /*status*/
      f[4] == "streaming"), (!o || _[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && Ye(
        e,
        "translucent",
        /*variant*/
        f[8] === "center" && /*status*/
        (f[4] === "pending" || /*status*/
        f[4] === "error") || /*translucent*/
        f[11] || /*show_progress*/
        f[6] === "minimal"
      ), (!o || _[0] & /*variant, show_progress, status, show_progress*/
      336) && Ye(
        e,
        "generating",
        /*status*/
        f[4] === "generating" && /*show_progress*/
        f[6] === "full"
      ), (!o || _[0] & /*variant, show_progress, border*/
      4416) && Ye(
        e,
        "border",
        /*border*/
        f[12]
      ), _[0] & /*absolute*/
      1024 && Ot(
        e,
        "position",
        /*absolute*/
        f[10] ? "absolute" : "static"
      ), _[0] & /*absolute*/
      1024 && Ot(
        e,
        "padding",
        /*absolute*/
        f[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(f) {
      o || (at(i), o = !0);
    },
    o(f) {
      wt(i), o = !1;
    },
    d(f) {
      f && R(e), ~t && s[t].d(), n[33](null);
    }
  };
}
var nf = function(n, e, t, i) {
  function l(o) {
    return o instanceof t ? o : new t(function(a) {
      a(o);
    });
  }
  return new (t || (t = Promise))(function(o, a) {
    function s(_) {
      try {
        f(i.next(_));
      } catch (d) {
        a(d);
      }
    }
    function r(_) {
      try {
        f(i.throw(_));
      } catch (d) {
        a(d);
      }
    }
    function f(_) {
      _.done ? o(_.value) : l(_.value).then(s, r);
    }
    f((i = i.apply(n, e || [])).next());
  });
};
let ei = [], Ei = !1;
const lf = typeof window < "u", Jo = lf ? window.requestAnimationFrame : (n) => {
};
function of(n) {
  return nf(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (ei.push(e), !Ei) Ei = !0;
      else return;
      yield Bs(), Jo(() => {
        let i = [0, 0];
        for (let l = 0; l < ei.length; l++) {
          const a = ei[l].getBoundingClientRect();
          (l === 0 || a.top + window.scrollY <= i[0]) && (i[0] = a.top + window.scrollY, i[1] = l);
        }
        window.scrollTo({ top: i[0] - 20, behavior: "smooth" }), Ei = !1, ei = [];
      });
    }
  });
}
function af(n, e, t) {
  let i, { $$slots: l = {}, $$scope: o } = e;
  this && this.__awaiter;
  const a = Ws();
  let { i18n: s } = e, { eta: r = null } = e, { queue_position: f } = e, { queue_size: _ } = e, { status: d } = e, { scroll_to_output: c = !1 } = e, { timer: u = !0 } = e, { show_progress: h = "full" } = e, { message: v = null } = e, { progress: T = null } = e, { variant: k = "default" } = e, { loading_text: w = "Loading..." } = e, { absolute: g = !0 } = e, { translucent: b = !1 } = e, { border: O = !1 } = e, { autoscroll: P } = e, U, j = !1, F = 0, L = 0, J = null, Y = null, ne = 0, B = null, ie, se = null, Oe = !0;
  const de = () => {
    t(0, r = t(27, J = t(19, K = null))), t(25, F = performance.now()), t(26, L = 0), j = !0, be();
  };
  function be() {
    Jo(() => {
      t(26, L = (performance.now() - F) / 1e3), j && be();
    });
  }
  function Le() {
    t(26, L = 0), t(0, r = t(27, J = t(19, K = null))), j && (j = !1);
  }
  Hs(() => {
    j && Le();
  });
  let K = null;
  function ve(S) {
    jl[S ? "unshift" : "push"](() => {
      se = S, t(16, se), t(7, T), t(14, B), t(15, ie);
    });
  }
  const X = () => {
    a("clear_status");
  };
  function le(S) {
    jl[S ? "unshift" : "push"](() => {
      U = S, t(13, U);
    });
  }
  return n.$$set = (S) => {
    "i18n" in S && t(1, s = S.i18n), "eta" in S && t(0, r = S.eta), "queue_position" in S && t(2, f = S.queue_position), "queue_size" in S && t(3, _ = S.queue_size), "status" in S && t(4, d = S.status), "scroll_to_output" in S && t(22, c = S.scroll_to_output), "timer" in S && t(5, u = S.timer), "show_progress" in S && t(6, h = S.show_progress), "message" in S && t(23, v = S.message), "progress" in S && t(7, T = S.progress), "variant" in S && t(8, k = S.variant), "loading_text" in S && t(9, w = S.loading_text), "absolute" in S && t(10, g = S.absolute), "translucent" in S && t(11, b = S.translucent), "border" in S && t(12, O = S.border), "autoscroll" in S && t(24, P = S.autoscroll), "$$scope" in S && t(29, o = S.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (r === null && t(0, r = J), r != null && J !== r && (t(28, Y = (performance.now() - F) / 1e3 + r), t(19, K = Y.toFixed(1)), t(27, J = r))), n.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, ne = Y === null || Y <= 0 || !L ? null : Math.min(L / Y, 1)), n.$$.dirty[0] & /*progress*/
    128 && T != null && t(18, Oe = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (T != null ? t(14, B = T.map((S) => {
      if (S.index != null && S.length != null)
        return S.index / S.length;
      if (S.progress != null)
        return S.progress;
    })) : t(14, B = null), B ? (t(15, ie = B[B.length - 1]), se && (ie === 0 ? t(16, se.style.transition = "0", se) : t(16, se.style.transition = "150ms", se))) : t(15, ie = void 0)), n.$$.dirty[0] & /*status*/
    16 && (d === "pending" ? de() : Le()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && U && c && (d === "pending" || d === "complete") && of(U, P), n.$$.dirty[0] & /*status, message*/
    8388624, n.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, i = L.toFixed(1));
  }, [
    r,
    s,
    f,
    _,
    d,
    u,
    h,
    T,
    k,
    w,
    g,
    b,
    O,
    U,
    B,
    ie,
    se,
    ne,
    Oe,
    K,
    i,
    a,
    c,
    v,
    P,
    F,
    L,
    J,
    Y,
    o,
    l,
    ve,
    X,
    le
  ];
}
class rf extends Us {
  constructor(e) {
    super(), zs(
      this,
      e,
      af,
      tf,
      qs,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
/*! @license DOMPurify 3.2.1 | (c) Cure53 and other contributors | Released under the Apache license 2.0 and Mozilla Public License 2.0 | github.com/cure53/DOMPurify/blob/3.2.1/LICENSE */
const {
  entries: Qo,
  setPrototypeOf: ro,
  isFrozen: sf,
  getPrototypeOf: ff,
  getOwnPropertyDescriptor: uf
} = Object;
let {
  freeze: Ne,
  seal: xe,
  create: xo
} = Object, {
  apply: Zi,
  construct: Ki
} = typeof Reflect < "u" && Reflect;
Ne || (Ne = function(e) {
  return e;
});
xe || (xe = function(e) {
  return e;
});
Zi || (Zi = function(e, t, i) {
  return e.apply(t, i);
});
Ki || (Ki = function(e, t) {
  return new e(...t);
});
const ti = Ve(Array.prototype.forEach), so = Ve(Array.prototype.pop), Ln = Ve(Array.prototype.push), ai = Ve(String.prototype.toLowerCase), Ti = Ve(String.prototype.toString), fo = Ve(String.prototype.match), Cn = Ve(String.prototype.replace), cf = Ve(String.prototype.indexOf), _f = Ve(String.prototype.trim), lt = Ve(Object.prototype.hasOwnProperty), Ie = Ve(RegExp.prototype.test), In = df(TypeError);
function Ve(n) {
  return function(e) {
    for (var t = arguments.length, i = new Array(t > 1 ? t - 1 : 0), l = 1; l < t; l++)
      i[l - 1] = arguments[l];
    return Zi(n, e, i);
  };
}
function df(n) {
  return function() {
    for (var e = arguments.length, t = new Array(e), i = 0; i < e; i++)
      t[i] = arguments[i];
    return Ki(n, t);
  };
}
function V(n, e) {
  let t = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : ai;
  ro && ro(n, null);
  let i = e.length;
  for (; i--; ) {
    let l = e[i];
    if (typeof l == "string") {
      const o = t(l);
      o !== l && (sf(e) || (e[i] = o), l = o);
    }
    n[l] = !0;
  }
  return n;
}
function mf(n) {
  for (let e = 0; e < n.length; e++)
    lt(n, e) || (n[e] = null);
  return n;
}
function Ht(n) {
  const e = xo(null);
  for (const [t, i] of Qo(n))
    lt(n, t) && (Array.isArray(i) ? e[t] = mf(i) : i && typeof i == "object" && i.constructor === Object ? e[t] = Ht(i) : e[t] = i);
  return e;
}
function Nn(n, e) {
  for (; n !== null; ) {
    const i = uf(n, e);
    if (i) {
      if (i.get)
        return Ve(i.get);
      if (typeof i.value == "function")
        return Ve(i.value);
    }
    n = ff(n);
  }
  function t() {
    return null;
  }
  return t;
}
const uo = Ne(["a", "abbr", "acronym", "address", "area", "article", "aside", "audio", "b", "bdi", "bdo", "big", "blink", "blockquote", "body", "br", "button", "canvas", "caption", "center", "cite", "code", "col", "colgroup", "content", "data", "datalist", "dd", "decorator", "del", "details", "dfn", "dialog", "dir", "div", "dl", "dt", "element", "em", "fieldset", "figcaption", "figure", "font", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html", "i", "img", "input", "ins", "kbd", "label", "legend", "li", "main", "map", "mark", "marquee", "menu", "menuitem", "meter", "nav", "nobr", "ol", "optgroup", "option", "output", "p", "picture", "pre", "progress", "q", "rp", "rt", "ruby", "s", "samp", "section", "select", "shadow", "small", "source", "spacer", "span", "strike", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "time", "tr", "track", "tt", "u", "ul", "var", "video", "wbr"]), Ai = Ne(["svg", "a", "altglyph", "altglyphdef", "altglyphitem", "animatecolor", "animatemotion", "animatetransform", "circle", "clippath", "defs", "desc", "ellipse", "filter", "font", "g", "glyph", "glyphref", "hkern", "image", "line", "lineargradient", "marker", "mask", "metadata", "mpath", "path", "pattern", "polygon", "polyline", "radialgradient", "rect", "stop", "style", "switch", "symbol", "text", "textpath", "title", "tref", "tspan", "view", "vkern"]), Si = Ne(["feBlend", "feColorMatrix", "feComponentTransfer", "feComposite", "feConvolveMatrix", "feDiffuseLighting", "feDisplacementMap", "feDistantLight", "feDropShadow", "feFlood", "feFuncA", "feFuncB", "feFuncG", "feFuncR", "feGaussianBlur", "feImage", "feMerge", "feMergeNode", "feMorphology", "feOffset", "fePointLight", "feSpecularLighting", "feSpotLight", "feTile", "feTurbulence"]), hf = Ne(["animate", "color-profile", "cursor", "discard", "font-face", "font-face-format", "font-face-name", "font-face-src", "font-face-uri", "foreignobject", "hatch", "hatchpath", "mesh", "meshgradient", "meshpatch", "meshrow", "missing-glyph", "script", "set", "solidcolor", "unknown", "use"]), Di = Ne(["math", "menclose", "merror", "mfenced", "mfrac", "mglyph", "mi", "mlabeledtr", "mmultiscripts", "mn", "mo", "mover", "mpadded", "mphantom", "mroot", "mrow", "ms", "mspace", "msqrt", "mstyle", "msub", "msup", "msubsup", "mtable", "mtd", "mtext", "mtr", "munder", "munderover", "mprescripts"]), gf = Ne(["maction", "maligngroup", "malignmark", "mlongdiv", "mscarries", "mscarry", "msgroup", "mstack", "msline", "msrow", "semantics", "annotation", "annotation-xml", "mprescripts", "none"]), co = Ne(["#text"]), _o = Ne(["accept", "action", "align", "alt", "autocapitalize", "autocomplete", "autopictureinpicture", "autoplay", "background", "bgcolor", "border", "capture", "cellpadding", "cellspacing", "checked", "cite", "class", "clear", "color", "cols", "colspan", "controls", "controlslist", "coords", "crossorigin", "datetime", "decoding", "default", "dir", "disabled", "disablepictureinpicture", "disableremoteplayback", "download", "draggable", "enctype", "enterkeyhint", "face", "for", "headers", "height", "hidden", "high", "href", "hreflang", "id", "inputmode", "integrity", "ismap", "kind", "label", "lang", "list", "loading", "loop", "low", "max", "maxlength", "media", "method", "min", "minlength", "multiple", "muted", "name", "nonce", "noshade", "novalidate", "nowrap", "open", "optimum", "pattern", "placeholder", "playsinline", "popover", "popovertarget", "popovertargetaction", "poster", "preload", "pubdate", "radiogroup", "readonly", "rel", "required", "rev", "reversed", "role", "rows", "rowspan", "spellcheck", "scope", "selected", "shape", "size", "sizes", "span", "srclang", "start", "src", "srcset", "step", "style", "summary", "tabindex", "title", "translate", "type", "usemap", "valign", "value", "width", "wrap", "xmlns", "slot"]), Li = Ne(["accent-height", "accumulate", "additive", "alignment-baseline", "amplitude", "ascent", "attributename", "attributetype", "azimuth", "basefrequency", "baseline-shift", "begin", "bias", "by", "class", "clip", "clippathunits", "clip-path", "clip-rule", "color", "color-interpolation", "color-interpolation-filters", "color-profile", "color-rendering", "cx", "cy", "d", "dx", "dy", "diffuseconstant", "direction", "display", "divisor", "dur", "edgemode", "elevation", "end", "exponent", "fill", "fill-opacity", "fill-rule", "filter", "filterunits", "flood-color", "flood-opacity", "font-family", "font-size", "font-size-adjust", "font-stretch", "font-style", "font-variant", "font-weight", "fx", "fy", "g1", "g2", "glyph-name", "glyphref", "gradientunits", "gradienttransform", "height", "href", "id", "image-rendering", "in", "in2", "intercept", "k", "k1", "k2", "k3", "k4", "kerning", "keypoints", "keysplines", "keytimes", "lang", "lengthadjust", "letter-spacing", "kernelmatrix", "kernelunitlength", "lighting-color", "local", "marker-end", "marker-mid", "marker-start", "markerheight", "markerunits", "markerwidth", "maskcontentunits", "maskunits", "max", "mask", "media", "method", "mode", "min", "name", "numoctaves", "offset", "operator", "opacity", "order", "orient", "orientation", "origin", "overflow", "paint-order", "path", "pathlength", "patterncontentunits", "patterntransform", "patternunits", "points", "preservealpha", "preserveaspectratio", "primitiveunits", "r", "rx", "ry", "radius", "refx", "refy", "repeatcount", "repeatdur", "restart", "result", "rotate", "scale", "seed", "shape-rendering", "slope", "specularconstant", "specularexponent", "spreadmethod", "startoffset", "stddeviation", "stitchtiles", "stop-color", "stop-opacity", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke", "stroke-width", "style", "surfacescale", "systemlanguage", "tabindex", "tablevalues", "targetx", "targety", "transform", "transform-origin", "text-anchor", "text-decoration", "text-rendering", "textlength", "type", "u1", "u2", "unicode", "values", "viewbox", "visibility", "version", "vert-adv-y", "vert-origin-x", "vert-origin-y", "width", "word-spacing", "wrap", "writing-mode", "xchannelselector", "ychannelselector", "x", "x1", "x2", "xmlns", "y", "y1", "y2", "z", "zoomandpan"]), mo = Ne(["accent", "accentunder", "align", "bevelled", "close", "columnsalign", "columnlines", "columnspan", "denomalign", "depth", "dir", "display", "displaystyle", "encoding", "fence", "frame", "height", "href", "id", "largeop", "length", "linethickness", "lspace", "lquote", "mathbackground", "mathcolor", "mathsize", "mathvariant", "maxsize", "minsize", "movablelimits", "notation", "numalign", "open", "rowalign", "rowlines", "rowspacing", "rowspan", "rspace", "rquote", "scriptlevel", "scriptminsize", "scriptsizemultiplier", "selection", "separator", "separators", "stretchy", "subscriptshift", "supscriptshift", "symmetric", "voffset", "width", "xmlns"]), ni = Ne(["xlink:href", "xml:id", "xlink:title", "xml:space", "xmlns:xlink"]), bf = xe(/\{\{[\w\W]*|[\w\W]*\}\}/gm), pf = xe(/<%[\w\W]*|[\w\W]*%>/gm), wf = xe(/\${[\w\W]*}/gm), vf = xe(/^data-[\-\w.\u00B7-\uFFFF]/), kf = xe(/^aria-[\-\w]+$/), $o = xe(
  /^(?:(?:(?:f|ht)tps?|mailto|tel|callto|sms|cid|xmpp):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i
  // eslint-disable-line no-useless-escape
), yf = xe(/^(?:\w+script|data):/i), Ef = xe(
  /[\u0000-\u0020\u00A0\u1680\u180E\u2000-\u2029\u205F\u3000]/g
  // eslint-disable-line no-control-regex
), ea = xe(/^html$/i), Tf = xe(/^[a-z][.\w]*(-[.\w]+)+$/i);
var ho = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  ARIA_ATTR: kf,
  ATTR_WHITESPACE: Ef,
  CUSTOM_ELEMENT: Tf,
  DATA_ATTR: vf,
  DOCTYPE_NAME: ea,
  ERB_EXPR: pf,
  IS_ALLOWED_URI: $o,
  IS_SCRIPT_OR_DATA: yf,
  MUSTACHE_EXPR: bf,
  TMPLIT_EXPR: wf
});
const On = {
  element: 1,
  attribute: 2,
  text: 3,
  cdataSection: 4,
  entityReference: 5,
  // Deprecated
  entityNode: 6,
  // Deprecated
  progressingInstruction: 7,
  comment: 8,
  document: 9,
  documentType: 10,
  documentFragment: 11,
  notation: 12
  // Deprecated
}, Af = function() {
  return typeof window > "u" ? null : window;
}, Sf = function(e, t) {
  if (typeof e != "object" || typeof e.createPolicy != "function")
    return null;
  let i = null;
  const l = "data-tt-policy-suffix";
  t && t.hasAttribute(l) && (i = t.getAttribute(l));
  const o = "dompurify" + (i ? "#" + i : "");
  try {
    return e.createPolicy(o, {
      createHTML(a) {
        return a;
      },
      createScriptURL(a) {
        return a;
      }
    });
  } catch {
    return console.warn("TrustedTypes policy " + o + " could not be created."), null;
  }
};
function ta() {
  let n = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : Af();
  const e = (I) => ta(I);
  if (e.version = "3.2.1", e.removed = [], !n || !n.document || n.document.nodeType !== On.document)
    return e.isSupported = !1, e;
  let {
    document: t
  } = n;
  const i = t, l = i.currentScript, {
    DocumentFragment: o,
    HTMLTemplateElement: a,
    Node: s,
    Element: r,
    NodeFilter: f,
    NamedNodeMap: _ = n.NamedNodeMap || n.MozNamedAttrMap,
    HTMLFormElement: d,
    DOMParser: c,
    trustedTypes: u
  } = n, h = r.prototype, v = Nn(h, "cloneNode"), T = Nn(h, "remove"), k = Nn(h, "nextSibling"), w = Nn(h, "childNodes"), g = Nn(h, "parentNode");
  if (typeof a == "function") {
    const I = t.createElement("template");
    I.content && I.content.ownerDocument && (t = I.content.ownerDocument);
  }
  let b, O = "";
  const {
    implementation: P,
    createNodeIterator: U,
    createDocumentFragment: j,
    getElementsByTagName: F
  } = t, {
    importNode: L
  } = i;
  let J = {};
  e.isSupported = typeof Qo == "function" && typeof g == "function" && P && P.createHTMLDocument !== void 0;
  const {
    MUSTACHE_EXPR: Y,
    ERB_EXPR: ne,
    TMPLIT_EXPR: B,
    DATA_ATTR: ie,
    ARIA_ATTR: se,
    IS_SCRIPT_OR_DATA: Oe,
    ATTR_WHITESPACE: de,
    CUSTOM_ELEMENT: be
  } = ho;
  let {
    IS_ALLOWED_URI: Le
  } = ho, K = null;
  const ve = V({}, [...uo, ...Ai, ...Si, ...Di, ...co]);
  let X = null;
  const le = V({}, [..._o, ...Li, ...mo, ...ni]);
  let S = Object.seal(xo(null, {
    tagNameCheck: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: null
    },
    attributeNameCheck: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: null
    },
    allowCustomizedBuiltInElements: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: !1
    }
  })), Te = null, pe = null, D = !0, Z = !0, ee = !1, y = !0, M = !1, H = !0, q = !1, x = !1, ce = !1, _e = !1, me = !1, Ae = !1, fe = !0, Re = !1;
  const vt = "user-content-";
  let Pt = !0, E = !1, Tt = {}, At = null;
  const Hn = V({}, ["annotation-xml", "audio", "colgroup", "desc", "foreignobject", "head", "iframe", "math", "mi", "mn", "mo", "ms", "mtext", "noembed", "noframes", "noscript", "plaintext", "script", "style", "svg", "template", "thead", "title", "video", "xmp"]);
  let Wn = null;
  const Vn = V({}, ["audio", "video", "img", "source", "image", "track"]);
  let yn = null;
  const Gn = V({}, ["alt", "class", "for", "id", "label", "name", "pattern", "placeholder", "role", "summary", "title", "value", "style", "xmlns"]), tn = "http://www.w3.org/1998/Math/MathML", nn = "http://www.w3.org/2000/svg", $e = "http://www.w3.org/1999/xhtml";
  let St = $e, En = !1, Tn = null;
  const mi = V({}, [tn, nn, $e], Ti);
  let ln = V({}, ["mi", "mo", "mn", "ms", "mtext"]), on = V({}, ["annotation-xml"]);
  const hi = V({}, ["title", "style", "font", "a", "script"]);
  let Ft = null;
  const gi = ["application/xhtml+xml", "text/html"], bi = "text/html";
  let he = null, Dt = null;
  const pi = t.createElement("form"), jn = function(m) {
    return m instanceof RegExp || m instanceof Function;
  }, An = function() {
    let m = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {};
    if (!(Dt && Dt === m)) {
      if ((!m || typeof m != "object") && (m = {}), m = Ht(m), Ft = // eslint-disable-next-line unicorn/prefer-includes
      gi.indexOf(m.PARSER_MEDIA_TYPE) === -1 ? bi : m.PARSER_MEDIA_TYPE, he = Ft === "application/xhtml+xml" ? Ti : ai, K = lt(m, "ALLOWED_TAGS") ? V({}, m.ALLOWED_TAGS, he) : ve, X = lt(m, "ALLOWED_ATTR") ? V({}, m.ALLOWED_ATTR, he) : le, Tn = lt(m, "ALLOWED_NAMESPACES") ? V({}, m.ALLOWED_NAMESPACES, Ti) : mi, yn = lt(m, "ADD_URI_SAFE_ATTR") ? V(Ht(Gn), m.ADD_URI_SAFE_ATTR, he) : Gn, Wn = lt(m, "ADD_DATA_URI_TAGS") ? V(Ht(Vn), m.ADD_DATA_URI_TAGS, he) : Vn, At = lt(m, "FORBID_CONTENTS") ? V({}, m.FORBID_CONTENTS, he) : Hn, Te = lt(m, "FORBID_TAGS") ? V({}, m.FORBID_TAGS, he) : {}, pe = lt(m, "FORBID_ATTR") ? V({}, m.FORBID_ATTR, he) : {}, Tt = lt(m, "USE_PROFILES") ? m.USE_PROFILES : !1, D = m.ALLOW_ARIA_ATTR !== !1, Z = m.ALLOW_DATA_ATTR !== !1, ee = m.ALLOW_UNKNOWN_PROTOCOLS || !1, y = m.ALLOW_SELF_CLOSE_IN_ATTR !== !1, M = m.SAFE_FOR_TEMPLATES || !1, H = m.SAFE_FOR_XML !== !1, q = m.WHOLE_DOCUMENT || !1, _e = m.RETURN_DOM || !1, me = m.RETURN_DOM_FRAGMENT || !1, Ae = m.RETURN_TRUSTED_TYPE || !1, ce = m.FORCE_BODY || !1, fe = m.SANITIZE_DOM !== !1, Re = m.SANITIZE_NAMED_PROPS || !1, Pt = m.KEEP_CONTENT !== !1, E = m.IN_PLACE || !1, Le = m.ALLOWED_URI_REGEXP || $o, St = m.NAMESPACE || $e, ln = m.MATHML_TEXT_INTEGRATION_POINTS || ln, on = m.HTML_INTEGRATION_POINTS || on, S = m.CUSTOM_ELEMENT_HANDLING || {}, m.CUSTOM_ELEMENT_HANDLING && jn(m.CUSTOM_ELEMENT_HANDLING.tagNameCheck) && (S.tagNameCheck = m.CUSTOM_ELEMENT_HANDLING.tagNameCheck), m.CUSTOM_ELEMENT_HANDLING && jn(m.CUSTOM_ELEMENT_HANDLING.attributeNameCheck) && (S.attributeNameCheck = m.CUSTOM_ELEMENT_HANDLING.attributeNameCheck), m.CUSTOM_ELEMENT_HANDLING && typeof m.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements == "boolean" && (S.allowCustomizedBuiltInElements = m.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements), M && (Z = !1), me && (_e = !0), Tt && (K = V({}, co), X = [], Tt.html === !0 && (V(K, uo), V(X, _o)), Tt.svg === !0 && (V(K, Ai), V(X, Li), V(X, ni)), Tt.svgFilters === !0 && (V(K, Si), V(X, Li), V(X, ni)), Tt.mathMl === !0 && (V(K, Di), V(X, mo), V(X, ni))), m.ADD_TAGS && (K === ve && (K = Ht(K)), V(K, m.ADD_TAGS, he)), m.ADD_ATTR && (X === le && (X = Ht(X)), V(X, m.ADD_ATTR, he)), m.ADD_URI_SAFE_ATTR && V(yn, m.ADD_URI_SAFE_ATTR, he), m.FORBID_CONTENTS && (At === Hn && (At = Ht(At)), V(At, m.FORBID_CONTENTS, he)), Pt && (K["#text"] = !0), q && V(K, ["html", "head", "body"]), K.table && (V(K, ["tbody"]), delete Te.tbody), m.TRUSTED_TYPES_POLICY) {
        if (typeof m.TRUSTED_TYPES_POLICY.createHTML != "function")
          throw In('TRUSTED_TYPES_POLICY configuration option must provide a "createHTML" hook.');
        if (typeof m.TRUSTED_TYPES_POLICY.createScriptURL != "function")
          throw In('TRUSTED_TYPES_POLICY configuration option must provide a "createScriptURL" hook.');
        b = m.TRUSTED_TYPES_POLICY, O = b.createHTML("");
      } else
        b === void 0 && (b = Sf(u, l)), b !== null && typeof O == "string" && (O = b.createHTML(""));
      Ne && Ne(m), Dt = m;
    }
  }, p = V({}, [...Ai, ...Si, ...hf]), te = V({}, [...Di, ...gf]), ge = function(m) {
    let A = g(m);
    (!A || !A.tagName) && (A = {
      namespaceURI: St,
      tagName: "template"
    });
    const C = ai(m.tagName), oe = ai(A.tagName);
    return Tn[m.namespaceURI] ? m.namespaceURI === nn ? A.namespaceURI === $e ? C === "svg" : A.namespaceURI === tn ? C === "svg" && (oe === "annotation-xml" || ln[oe]) : !!p[C] : m.namespaceURI === tn ? A.namespaceURI === $e ? C === "math" : A.namespaceURI === nn ? C === "math" && on[oe] : !!te[C] : m.namespaceURI === $e ? A.namespaceURI === nn && !on[oe] || A.namespaceURI === tn && !ln[oe] ? !1 : !te[C] && (hi[C] || !p[C]) : !!(Ft === "application/xhtml+xml" && Tn[m.namespaceURI]) : !1;
  }, $ = function(m) {
    Ln(e.removed, {
      element: m
    });
    try {
      g(m).removeChild(m);
    } catch {
      T(m);
    }
  }, st = function(m, A) {
    try {
      Ln(e.removed, {
        attribute: A.getAttributeNode(m),
        from: A
      });
    } catch {
      Ln(e.removed, {
        attribute: null,
        from: A
      });
    }
    if (A.removeAttribute(m), m === "is" && !X[m])
      if (_e || me)
        try {
          $(A);
        } catch {
        }
      else
        try {
          A.setAttribute(m, "");
        } catch {
        }
  }, Lt = function(m) {
    let A = null, C = null;
    if (ce)
      m = "<remove></remove>" + m;
    else {
      const ke = fo(m, /^[\r\n\t ]+/);
      C = ke && ke[0];
    }
    Ft === "application/xhtml+xml" && St === $e && (m = '<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>' + m + "</body></html>");
    const oe = b ? b.createHTML(m) : m;
    if (St === $e)
      try {
        A = new c().parseFromString(oe, Ft);
      } catch {
      }
    if (!A || !A.documentElement) {
      A = P.createDocument(St, "template", null);
      try {
        A.documentElement.innerHTML = En ? O : oe;
      } catch {
      }
    }
    const Se = A.body || A.documentElement;
    return m && C && Se.insertBefore(t.createTextNode(C), Se.childNodes[0] || null), St === $e ? F.call(A, q ? "html" : "body")[0] : q ? A.documentElement : Se;
  }, Ut = function(m) {
    return U.call(
      m.ownerDocument || m,
      m,
      // eslint-disable-next-line no-bitwise
      f.SHOW_ELEMENT | f.SHOW_COMMENT | f.SHOW_TEXT | f.SHOW_PROCESSING_INSTRUCTION | f.SHOW_CDATA_SECTION,
      null
    );
  }, Yn = function(m) {
    return m instanceof d && (typeof m.nodeName != "string" || typeof m.textContent != "string" || typeof m.removeChild != "function" || !(m.attributes instanceof _) || typeof m.removeAttribute != "function" || typeof m.setAttribute != "function" || typeof m.namespaceURI != "string" || typeof m.insertBefore != "function" || typeof m.hasChildNodes != "function");
  }, Xn = function(m) {
    return typeof s == "function" && m instanceof s;
  };
  function qe(I, m, A) {
    J[I] && ti(J[I], (C) => {
      C.call(e, m, A, Dt);
    });
  }
  const ft = function(m) {
    let A = null;
    if (qe("beforeSanitizeElements", m, null), Yn(m))
      return $(m), !0;
    const C = he(m.nodeName);
    if (qe("uponSanitizeElement", m, {
      tagName: C,
      allowedTags: K
    }), m.hasChildNodes() && !Xn(m.firstElementChild) && Ie(/<[/\w]/g, m.innerHTML) && Ie(/<[/\w]/g, m.textContent) || m.nodeType === On.progressingInstruction || H && m.nodeType === On.comment && Ie(/<[/\w]/g, m.data))
      return $(m), !0;
    if (!K[C] || Te[C]) {
      if (!Te[C] && el(C) && (S.tagNameCheck instanceof RegExp && Ie(S.tagNameCheck, C) || S.tagNameCheck instanceof Function && S.tagNameCheck(C)))
        return !1;
      if (Pt && !At[C]) {
        const oe = g(m) || m.parentNode, Se = w(m) || m.childNodes;
        if (Se && oe) {
          const ke = Se.length;
          for (let Me = ke - 1; Me >= 0; --Me) {
            const ut = v(Se[Me], !0);
            ut.__removalCount = (m.__removalCount || 0) + 1, oe.insertBefore(ut, k(m));
          }
        }
      }
      return $(m), !0;
    }
    return m instanceof r && !ge(m) || (C === "noscript" || C === "noembed" || C === "noframes") && Ie(/<\/no(script|embed|frames)/i, m.innerHTML) ? ($(m), !0) : (M && m.nodeType === On.text && (A = m.textContent, ti([Y, ne, B], (oe) => {
      A = Cn(A, oe, " ");
    }), m.textContent !== A && (Ln(e.removed, {
      element: m.cloneNode()
    }), m.textContent = A)), qe("afterSanitizeElements", m, null), !1);
  }, an = function(m, A, C) {
    if (fe && (A === "id" || A === "name") && (C in t || C in pi))
      return !1;
    if (!(Z && !pe[A] && Ie(ie, A))) {
      if (!(D && Ie(se, A))) {
        if (!X[A] || pe[A]) {
          if (
            // First condition does a very basic check if a) it's basically a valid custom element tagname AND
            // b) if the tagName passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
            // and c) if the attribute name passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.attributeNameCheck
            !(el(m) && (S.tagNameCheck instanceof RegExp && Ie(S.tagNameCheck, m) || S.tagNameCheck instanceof Function && S.tagNameCheck(m)) && (S.attributeNameCheck instanceof RegExp && Ie(S.attributeNameCheck, A) || S.attributeNameCheck instanceof Function && S.attributeNameCheck(A)) || // Alternative, second condition checks if it's an `is`-attribute, AND
            // the value passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
            A === "is" && S.allowCustomizedBuiltInElements && (S.tagNameCheck instanceof RegExp && Ie(S.tagNameCheck, C) || S.tagNameCheck instanceof Function && S.tagNameCheck(C)))
          ) return !1;
        } else if (!yn[A]) {
          if (!Ie(Le, Cn(C, de, ""))) {
            if (!((A === "src" || A === "xlink:href" || A === "href") && m !== "script" && cf(C, "data:") === 0 && Wn[m])) {
              if (!(ee && !Ie(Oe, Cn(C, de, "")))) {
                if (C)
                  return !1;
              }
            }
          }
        }
      }
    }
    return !0;
  }, el = function(m) {
    return m !== "annotation-xml" && fo(m, be);
  }, tl = function(m) {
    qe("beforeSanitizeAttributes", m, null);
    const {
      attributes: A
    } = m;
    if (!A)
      return;
    const C = {
      attrName: "",
      attrValue: "",
      keepAttr: !0,
      allowedAttributes: X,
      forceKeepAttr: void 0
    };
    let oe = A.length;
    for (; oe--; ) {
      const Se = A[oe], {
        name: ke,
        namespaceURI: Me,
        value: ut
      } = Se, Sn = he(ke);
      let Ce = ke === "value" ? ut : _f(ut);
      if (C.attrName = Sn, C.attrValue = Ce, C.keepAttr = !0, C.forceKeepAttr = void 0, qe("uponSanitizeAttribute", m, C), Ce = C.attrValue, Re && (Sn === "id" || Sn === "name") && (st(ke, m), Ce = vt + Ce), H && Ie(/((--!?|])>)|<\/(style|title)/i, Ce)) {
        st(ke, m);
        continue;
      }
      if (C.forceKeepAttr || (st(ke, m), !C.keepAttr))
        continue;
      if (!y && Ie(/\/>/i, Ce)) {
        st(ke, m);
        continue;
      }
      M && ti([Y, ne, B], (il) => {
        Ce = Cn(Ce, il, " ");
      });
      const nl = he(m.nodeName);
      if (an(nl, Sn, Ce)) {
        if (b && typeof u == "object" && typeof u.getAttributeType == "function" && !Me)
          switch (u.getAttributeType(nl, Sn)) {
            case "TrustedHTML": {
              Ce = b.createHTML(Ce);
              break;
            }
            case "TrustedScriptURL": {
              Ce = b.createScriptURL(Ce);
              break;
            }
          }
        try {
          Me ? m.setAttributeNS(Me, ke, Ce) : m.setAttribute(ke, Ce), Yn(m) ? $(m) : so(e.removed);
        } catch {
        }
      }
    }
    qe("afterSanitizeAttributes", m, null);
  }, na = function I(m) {
    let A = null;
    const C = Ut(m);
    for (qe("beforeSanitizeShadowDOM", m, null); A = C.nextNode(); )
      qe("uponSanitizeShadowNode", A, null), !ft(A) && (A.content instanceof o && I(A.content), tl(A));
    qe("afterSanitizeShadowDOM", m, null);
  };
  return e.sanitize = function(I) {
    let m = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {}, A = null, C = null, oe = null, Se = null;
    if (En = !I, En && (I = "<!-->"), typeof I != "string" && !Xn(I))
      if (typeof I.toString == "function") {
        if (I = I.toString(), typeof I != "string")
          throw In("dirty is not a string, aborting");
      } else
        throw In("toString is not a function");
    if (!e.isSupported)
      return I;
    if (x || An(m), e.removed = [], typeof I == "string" && (E = !1), E) {
      if (I.nodeName) {
        const ut = he(I.nodeName);
        if (!K[ut] || Te[ut])
          throw In("root node is forbidden and cannot be sanitized in-place");
      }
    } else if (I instanceof s)
      A = Lt("<!---->"), C = A.ownerDocument.importNode(I, !0), C.nodeType === On.element && C.nodeName === "BODY" || C.nodeName === "HTML" ? A = C : A.appendChild(C);
    else {
      if (!_e && !M && !q && // eslint-disable-next-line unicorn/prefer-includes
      I.indexOf("<") === -1)
        return b && Ae ? b.createHTML(I) : I;
      if (A = Lt(I), !A)
        return _e ? null : Ae ? O : "";
    }
    A && ce && $(A.firstChild);
    const ke = Ut(E ? I : A);
    for (; oe = ke.nextNode(); )
      ft(oe) || (oe.content instanceof o && na(oe.content), tl(oe));
    if (E)
      return I;
    if (_e) {
      if (me)
        for (Se = j.call(A.ownerDocument); A.firstChild; )
          Se.appendChild(A.firstChild);
      else
        Se = A;
      return (X.shadowroot || X.shadowrootmode) && (Se = L.call(i, Se, !0)), Se;
    }
    let Me = q ? A.outerHTML : A.innerHTML;
    return q && K["!doctype"] && A.ownerDocument && A.ownerDocument.doctype && A.ownerDocument.doctype.name && Ie(ea, A.ownerDocument.doctype.name) && (Me = "<!DOCTYPE " + A.ownerDocument.doctype.name + `>
` + Me), M && ti([Y, ne, B], (ut) => {
      Me = Cn(Me, ut, " ");
    }), b && Ae ? b.createHTML(Me) : Me;
  }, e.setConfig = function() {
    let I = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {};
    An(I), x = !0;
  }, e.clearConfig = function() {
    Dt = null, x = !1;
  }, e.isValidAttribute = function(I, m, A) {
    Dt || An({});
    const C = he(I), oe = he(m);
    return an(C, oe, A);
  }, e.addHook = function(I, m) {
    typeof m == "function" && (J[I] = J[I] || [], Ln(J[I], m));
  }, e.removeHook = function(I) {
    if (J[I])
      return so(J[I]);
  }, e.removeHooks = function(I) {
    J[I] && (J[I] = []);
  }, e.removeAllHooks = function() {
    J = {};
  }, e;
}
ta();
const {
  SvelteComponent: Df,
  add_flush_callback: Ci,
  assign: Lf,
  bind: Ii,
  binding_callbacks: Ni,
  check_outros: Cf,
  claim_component: Ji,
  claim_space: If,
  create_component: Qi,
  destroy_component: xi,
  detach: Nf,
  flush: G,
  get_spread_object: Of,
  get_spread_update: Rf,
  group_outros: Mf,
  init: Pf,
  insert_hydration: Ff,
  mount_component: $i,
  safe_not_equal: Uf,
  space: zf,
  transition_in: mn,
  transition_out: zn
} = window.__gradio__svelte__internal;
function go(n) {
  let e, t;
  const i = [
    { autoscroll: (
      /*gradio*/
      n[2].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      n[2].i18n
    ) },
    /*loading_status*/
    n[20]
  ];
  let l = {};
  for (let o = 0; o < i.length; o += 1)
    l = Lf(l, i[o]);
  return e = new rf({ props: l }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    n[39]
  ), {
    c() {
      Qi(e.$$.fragment);
    },
    l(o) {
      Ji(e.$$.fragment, o);
    },
    m(o, a) {
      $i(e, o, a), t = !0;
    },
    p(o, a) {
      const s = a[0] & /*gradio, loading_status*/
      1048580 ? Rf(i, [
        a[0] & /*gradio*/
        4 && { autoscroll: (
          /*gradio*/
          o[2].autoscroll
        ) },
        a[0] & /*gradio*/
        4 && { i18n: (
          /*gradio*/
          o[2].i18n
        ) },
        a[0] & /*loading_status*/
        1048576 && Of(
          /*loading_status*/
          o[20]
        )
      ]) : {};
      e.$set(s);
    },
    i(o) {
      t || (mn(e.$$.fragment, o), t = !0);
    },
    o(o) {
      zn(e.$$.fragment, o), t = !1;
    },
    d(o) {
      xi(e, o);
    }
  };
}
function qf(n) {
  let e, t, i, l, o, a, s = (
    /*loading_status*/
    n[20] && go(n)
  );
  function r(c) {
    n[42](c);
  }
  function f(c) {
    n[43](c);
  }
  function _(c) {
    n[44](c);
  }
  let d = {
    file_types: (
      /*file_types*/
      n[6]
    ),
    root: (
      /*root*/
      n[26]
    ),
    label: (
      /*label*/
      n[9]
    ),
    info: (
      /*info*/
      n[10]
    ),
    show_label: (
      /*show_label*/
      n[11]
    ),
    lines: (
      /*lines*/
      n[7]
    ),
    rtl: (
      /*rtl*/
      n[21]
    ),
    text_align: (
      /*text_align*/
      n[22]
    ),
    max_lines: /*max_lines*/ n[12] ? (
      /*max_lines*/
      n[12]
    ) : (
      /*lines*/
      n[7] + 1
    ),
    placeholder: (
      /*placeholder*/
      n[8]
    ),
    upload_btn: (
      /*upload_btn*/
      n[16]
    ),
    submit_btn: (
      /*submit_btn*/
      n[17]
    ),
    stop_btn: (
      /*stop_btn*/
      n[18]
    ),
    autofocus: (
      /*autofocus*/
      n[23]
    ),
    container: (
      /*container*/
      n[13]
    ),
    autoscroll: (
      /*autoscroll*/
      n[24]
    ),
    file_count: (
      /*file_count*/
      n[27]
    ),
    interactive: (
      /*interactive*/
      n[25]
    ),
    loading_message: (
      /*loading_message*/
      n[19]
    ),
    audio_btn: (
      /*audio_btn*/
      n[28]
    ),
    stop_audio_btn: (
      /*stop_audio_btn*/
      n[29]
    ),
    max_file_size: (
      /*gradio*/
      n[2].max_file_size
    ),
    on_change_cb: (
      /*on_change_cb*/
      n[38]
    ),
    server: (
      /*server*/
      n[36]
    ),
    rtc_configuration: (
      /*rtc_configuration*/
      n[30]
    ),
    time_limit: (
      /*time_limit*/
      n[31]
    ),
    track_constraints: (
      /*track_constraints*/
      n[35]
    ),
    mode: (
      /*mode*/
      n[33]
    ),
    rtp_params: (
      /*rtp_params*/
      n[34]
    ),
    modality: (
      /*modality*/
      n[32]
    ),
    gradio: (
      /*gradio*/
      n[2]
    ),
    upload: (
      /*func*/
      n[40]
    ),
    stream_handler: (
      /*func_1*/
      n[41]
    )
  };
  return (
    /*value*/
    n[0] !== void 0 && (d.value = /*value*/
    n[0]), /*value_is_output*/
    n[1] !== void 0 && (d.value_is_output = /*value_is_output*/
    n[1]), /*dragging*/
    n[37] !== void 0 && (d.dragging = /*dragging*/
    n[37]), t = new Es({ props: d }), Ni.push(() => Ii(t, "value", r)), Ni.push(() => Ii(t, "value_is_output", f)), Ni.push(() => Ii(t, "dragging", _)), t.$on(
      "tick",
      /*tick_handler*/
      n[45]
    ), t.$on(
      "change",
      /*change_handler*/
      n[46]
    ), t.$on(
      "input",
      /*input_handler*/
      n[47]
    ), t.$on(
      "submit",
      /*submit_handler*/
      n[48]
    ), t.$on(
      "stop",
      /*stop_handler*/
      n[49]
    ), t.$on(
      "blur",
      /*blur_handler*/
      n[50]
    ), t.$on(
      "select",
      /*select_handler*/
      n[51]
    ), t.$on(
      "focus",
      /*focus_handler*/
      n[52]
    ), t.$on(
      "upload",
      /*upload_handler*/
      n[53]
    ), t.$on(
      "error",
      /*error_handler*/
      n[54]
    ), t.$on(
      "start_recording",
      /*start_recording_handler*/
      n[55]
    ), t.$on(
      "stop_recording",
      /*stop_recording_handler*/
      n[56]
    ), {
      c() {
        s && s.c(), e = zf(), Qi(t.$$.fragment);
      },
      l(c) {
        s && s.l(c), e = If(c), Ji(t.$$.fragment, c);
      },
      m(c, u) {
        s && s.m(c, u), Ff(c, e, u), $i(t, c, u), a = !0;
      },
      p(c, u) {
        /*loading_status*/
        c[20] ? s ? (s.p(c, u), u[0] & /*loading_status*/
        1048576 && mn(s, 1)) : (s = go(c), s.c(), mn(s, 1), s.m(e.parentNode, e)) : s && (Mf(), zn(s, 1, 1, () => {
          s = null;
        }), Cf());
        const h = {};
        u[0] & /*file_types*/
        64 && (h.file_types = /*file_types*/
        c[6]), u[0] & /*root*/
        67108864 && (h.root = /*root*/
        c[26]), u[0] & /*label*/
        512 && (h.label = /*label*/
        c[9]), u[0] & /*info*/
        1024 && (h.info = /*info*/
        c[10]), u[0] & /*show_label*/
        2048 && (h.show_label = /*show_label*/
        c[11]), u[0] & /*lines*/
        128 && (h.lines = /*lines*/
        c[7]), u[0] & /*rtl*/
        2097152 && (h.rtl = /*rtl*/
        c[21]), u[0] & /*text_align*/
        4194304 && (h.text_align = /*text_align*/
        c[22]), u[0] & /*max_lines, lines*/
        4224 && (h.max_lines = /*max_lines*/
        c[12] ? (
          /*max_lines*/
          c[12]
        ) : (
          /*lines*/
          c[7] + 1
        )), u[0] & /*placeholder*/
        256 && (h.placeholder = /*placeholder*/
        c[8]), u[0] & /*upload_btn*/
        65536 && (h.upload_btn = /*upload_btn*/
        c[16]), u[0] & /*submit_btn*/
        131072 && (h.submit_btn = /*submit_btn*/
        c[17]), u[0] & /*stop_btn*/
        262144 && (h.stop_btn = /*stop_btn*/
        c[18]), u[0] & /*autofocus*/
        8388608 && (h.autofocus = /*autofocus*/
        c[23]), u[0] & /*container*/
        8192 && (h.container = /*container*/
        c[13]), u[0] & /*autoscroll*/
        16777216 && (h.autoscroll = /*autoscroll*/
        c[24]), u[0] & /*file_count*/
        134217728 && (h.file_count = /*file_count*/
        c[27]), u[0] & /*interactive*/
        33554432 && (h.interactive = /*interactive*/
        c[25]), u[0] & /*loading_message*/
        524288 && (h.loading_message = /*loading_message*/
        c[19]), u[0] & /*audio_btn*/
        268435456 && (h.audio_btn = /*audio_btn*/
        c[28]), u[0] & /*stop_audio_btn*/
        536870912 && (h.stop_audio_btn = /*stop_audio_btn*/
        c[29]), u[0] & /*gradio*/
        4 && (h.max_file_size = /*gradio*/
        c[2].max_file_size), u[1] & /*server*/
        32 && (h.server = /*server*/
        c[36]), u[0] & /*rtc_configuration*/
        1073741824 && (h.rtc_configuration = /*rtc_configuration*/
        c[30]), u[1] & /*time_limit*/
        1 && (h.time_limit = /*time_limit*/
        c[31]), u[1] & /*track_constraints*/
        16 && (h.track_constraints = /*track_constraints*/
        c[35]), u[1] & /*mode*/
        4 && (h.mode = /*mode*/
        c[33]), u[1] & /*rtp_params*/
        8 && (h.rtp_params = /*rtp_params*/
        c[34]), u[1] & /*modality*/
        2 && (h.modality = /*modality*/
        c[32]), u[0] & /*gradio*/
        4 && (h.gradio = /*gradio*/
        c[2]), u[0] & /*gradio*/
        4 && (h.upload = /*func*/
        c[40]), u[0] & /*gradio*/
        4 && (h.stream_handler = /*func_1*/
        c[41]), !i && u[0] & /*value*/
        1 && (i = !0, h.value = /*value*/
        c[0], Ci(() => i = !1)), !l && u[0] & /*value_is_output*/
        2 && (l = !0, h.value_is_output = /*value_is_output*/
        c[1], Ci(() => l = !1)), !o && u[1] & /*dragging*/
        64 && (o = !0, h.dragging = /*dragging*/
        c[37], Ci(() => o = !1)), t.$set(h);
      },
      i(c) {
        a || (mn(s), mn(t.$$.fragment, c), a = !0);
      },
      o(c) {
        zn(s), zn(t.$$.fragment, c), a = !1;
      },
      d(c) {
        c && Nf(e), s && s.d(c), xi(t, c);
      }
    }
  );
}
function Bf(n) {
  let e, t;
  return e = new Qa({
    props: {
      visible: (
        /*visible*/
        n[5]
      ),
      elem_id: (
        /*elem_id*/
        n[3]
      ),
      elem_classes: [.../*elem_classes*/
      n[4], "multimodal-textbox"],
      scale: (
        /*scale*/
        n[14]
      ),
      min_width: (
        /*min_width*/
        n[15]
      ),
      allow_overflow: !1,
      padding: (
        /*container*/
        n[13]
      ),
      border_mode: (
        /*dragging*/
        n[37] ? "focus" : "base"
      ),
      $$slots: { default: [qf] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      Qi(e.$$.fragment);
    },
    l(i) {
      Ji(e.$$.fragment, i);
    },
    m(i, l) {
      $i(e, i, l), t = !0;
    },
    p(i, l) {
      const o = {};
      l[0] & /*visible*/
      32 && (o.visible = /*visible*/
      i[5]), l[0] & /*elem_id*/
      8 && (o.elem_id = /*elem_id*/
      i[3]), l[0] & /*elem_classes*/
      16 && (o.elem_classes = [.../*elem_classes*/
      i[4], "multimodal-textbox"]), l[0] & /*scale*/
      16384 && (o.scale = /*scale*/
      i[14]), l[0] & /*min_width*/
      32768 && (o.min_width = /*min_width*/
      i[15]), l[0] & /*container*/
      8192 && (o.padding = /*container*/
      i[13]), l[1] & /*dragging*/
      64 && (o.border_mode = /*dragging*/
      i[37] ? "focus" : "base"), l[0] & /*file_types, root, label, info, show_label, lines, rtl, text_align, max_lines, placeholder, upload_btn, submit_btn, stop_btn, autofocus, container, autoscroll, file_count, interactive, loading_message, audio_btn, stop_audio_btn, gradio, rtc_configuration, value, value_is_output, loading_status*/
      2147434439 | l[1] & /*$$scope, server, time_limit, track_constraints, mode, rtp_params, modality, dragging*/
      67108991 && (o.$$scope = { dirty: l, ctx: i }), e.$set(o);
    },
    i(i) {
      t || (mn(e.$$.fragment, i), t = !0);
    },
    o(i) {
      zn(e.$$.fragment, i), t = !1;
    },
    d(i) {
      xi(e, i);
    }
  };
}
function Hf(n, e, t) {
  let { gradio: i } = e, { elem_id: l = "" } = e, { elem_classes: o = [] } = e, { visible: a = !0 } = e, { value: s = {
    text: "",
    files: [],
    audio: "__webrtc_value__"
  } } = e, { file_types: r = null } = e, { lines: f } = e, { placeholder: _ = "" } = e, { label: d = "MultimodalTextbox" } = e, { info: c = void 0 } = e, { show_label: u } = e, { max_lines: h } = e, { container: v = !0 } = e, { scale: T = null } = e, { min_width: k = void 0 } = e, { upload_btn: w = null } = e, { submit_btn: g = null } = e, { stop_btn: b = null } = e, { loading_message: O = "... Loading files ..." } = e, { loading_status: P = void 0 } = e, { value_is_output: U = !1 } = e, { rtl: j = !1 } = e, { text_align: F = void 0 } = e, { autofocus: L = !1 } = e, { autoscroll: J = !0 } = e, { interactive: Y } = e, { root: ne } = e, { file_count: B } = e, { audio_btn: ie } = e, { stop_audio_btn: se } = e, { rtc_configuration: Oe } = e, { time_limit: de = null } = e, { modality: be = "audio" } = e, { mode: Le = "send-receive" } = e, { rtp_params: K = {} } = e, { track_constraints: ve = {} } = e, { server: X } = e;
  const le = (E) => {
    i.dispatch(E === "change" ? "state_change" : "tick");
  };
  let S;
  const Te = () => i.dispatch("clear_status", P), pe = (...E) => i.client.upload(...E), D = (...E) => i.client.stream(...E);
  function Z(E) {
    s = E, t(0, s);
  }
  function ee(E) {
    U = E, t(1, U);
  }
  function y(E) {
    S = E, t(37, S);
  }
  const M = () => i.dispatch("tick"), H = () => i.dispatch("change", s), q = () => i.dispatch("input"), x = () => i.dispatch("submit"), ce = () => i.dispatch("stop"), _e = () => i.dispatch("blur"), me = (E) => i.dispatch("select", E.detail), Ae = () => i.dispatch("focus"), fe = ({ detail: E }) => i.dispatch("upload", E), Re = ({ detail: E }) => {
    i.dispatch("error", E);
  }, vt = () => i.dispatch("start_recording"), Pt = () => i.dispatch("stop_recording");
  return n.$$set = (E) => {
    "gradio" in E && t(2, i = E.gradio), "elem_id" in E && t(3, l = E.elem_id), "elem_classes" in E && t(4, o = E.elem_classes), "visible" in E && t(5, a = E.visible), "value" in E && t(0, s = E.value), "file_types" in E && t(6, r = E.file_types), "lines" in E && t(7, f = E.lines), "placeholder" in E && t(8, _ = E.placeholder), "label" in E && t(9, d = E.label), "info" in E && t(10, c = E.info), "show_label" in E && t(11, u = E.show_label), "max_lines" in E && t(12, h = E.max_lines), "container" in E && t(13, v = E.container), "scale" in E && t(14, T = E.scale), "min_width" in E && t(15, k = E.min_width), "upload_btn" in E && t(16, w = E.upload_btn), "submit_btn" in E && t(17, g = E.submit_btn), "stop_btn" in E && t(18, b = E.stop_btn), "loading_message" in E && t(19, O = E.loading_message), "loading_status" in E && t(20, P = E.loading_status), "value_is_output" in E && t(1, U = E.value_is_output), "rtl" in E && t(21, j = E.rtl), "text_align" in E && t(22, F = E.text_align), "autofocus" in E && t(23, L = E.autofocus), "autoscroll" in E && t(24, J = E.autoscroll), "interactive" in E && t(25, Y = E.interactive), "root" in E && t(26, ne = E.root), "file_count" in E && t(27, B = E.file_count), "audio_btn" in E && t(28, ie = E.audio_btn), "stop_audio_btn" in E && t(29, se = E.stop_audio_btn), "rtc_configuration" in E && t(30, Oe = E.rtc_configuration), "time_limit" in E && t(31, de = E.time_limit), "modality" in E && t(32, be = E.modality), "mode" in E && t(33, Le = E.mode), "rtp_params" in E && t(34, K = E.rtp_params), "track_constraints" in E && t(35, ve = E.track_constraints), "server" in E && t(36, X = E.server);
  }, [
    s,
    U,
    i,
    l,
    o,
    a,
    r,
    f,
    _,
    d,
    c,
    u,
    h,
    v,
    T,
    k,
    w,
    g,
    b,
    O,
    P,
    j,
    F,
    L,
    J,
    Y,
    ne,
    B,
    ie,
    se,
    Oe,
    de,
    be,
    Le,
    K,
    ve,
    X,
    S,
    le,
    Te,
    pe,
    D,
    Z,
    ee,
    y,
    M,
    H,
    q,
    x,
    ce,
    _e,
    me,
    Ae,
    fe,
    Re,
    vt,
    Pt
  ];
}
class Gf extends Df {
  constructor(e) {
    super(), Pf(
      this,
      e,
      Hf,
      Bf,
      Uf,
      {
        gradio: 2,
        elem_id: 3,
        elem_classes: 4,
        visible: 5,
        value: 0,
        file_types: 6,
        lines: 7,
        placeholder: 8,
        label: 9,
        info: 10,
        show_label: 11,
        max_lines: 12,
        container: 13,
        scale: 14,
        min_width: 15,
        upload_btn: 16,
        submit_btn: 17,
        stop_btn: 18,
        loading_message: 19,
        loading_status: 20,
        value_is_output: 1,
        rtl: 21,
        text_align: 22,
        autofocus: 23,
        autoscroll: 24,
        interactive: 25,
        root: 26,
        file_count: 27,
        audio_btn: 28,
        stop_audio_btn: 29,
        rtc_configuration: 30,
        time_limit: 31,
        modality: 32,
        mode: 33,
        rtp_params: 34,
        track_constraints: 35,
        server: 36
      },
      null,
      [-1, -1]
    );
  }
  get gradio() {
    return this.$$.ctx[2];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), G();
  }
  get elem_id() {
    return this.$$.ctx[3];
  }
  set elem_id(e) {
    this.$$set({ elem_id: e }), G();
  }
  get elem_classes() {
    return this.$$.ctx[4];
  }
  set elem_classes(e) {
    this.$$set({ elem_classes: e }), G();
  }
  get visible() {
    return this.$$.ctx[5];
  }
  set visible(e) {
    this.$$set({ visible: e }), G();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({ value: e }), G();
  }
  get file_types() {
    return this.$$.ctx[6];
  }
  set file_types(e) {
    this.$$set({ file_types: e }), G();
  }
  get lines() {
    return this.$$.ctx[7];
  }
  set lines(e) {
    this.$$set({ lines: e }), G();
  }
  get placeholder() {
    return this.$$.ctx[8];
  }
  set placeholder(e) {
    this.$$set({ placeholder: e }), G();
  }
  get label() {
    return this.$$.ctx[9];
  }
  set label(e) {
    this.$$set({ label: e }), G();
  }
  get info() {
    return this.$$.ctx[10];
  }
  set info(e) {
    this.$$set({ info: e }), G();
  }
  get show_label() {
    return this.$$.ctx[11];
  }
  set show_label(e) {
    this.$$set({ show_label: e }), G();
  }
  get max_lines() {
    return this.$$.ctx[12];
  }
  set max_lines(e) {
    this.$$set({ max_lines: e }), G();
  }
  get container() {
    return this.$$.ctx[13];
  }
  set container(e) {
    this.$$set({ container: e }), G();
  }
  get scale() {
    return this.$$.ctx[14];
  }
  set scale(e) {
    this.$$set({ scale: e }), G();
  }
  get min_width() {
    return this.$$.ctx[15];
  }
  set min_width(e) {
    this.$$set({ min_width: e }), G();
  }
  get upload_btn() {
    return this.$$.ctx[16];
  }
  set upload_btn(e) {
    this.$$set({ upload_btn: e }), G();
  }
  get submit_btn() {
    return this.$$.ctx[17];
  }
  set submit_btn(e) {
    this.$$set({ submit_btn: e }), G();
  }
  get stop_btn() {
    return this.$$.ctx[18];
  }
  set stop_btn(e) {
    this.$$set({ stop_btn: e }), G();
  }
  get loading_message() {
    return this.$$.ctx[19];
  }
  set loading_message(e) {
    this.$$set({ loading_message: e }), G();
  }
  get loading_status() {
    return this.$$.ctx[20];
  }
  set loading_status(e) {
    this.$$set({ loading_status: e }), G();
  }
  get value_is_output() {
    return this.$$.ctx[1];
  }
  set value_is_output(e) {
    this.$$set({ value_is_output: e }), G();
  }
  get rtl() {
    return this.$$.ctx[21];
  }
  set rtl(e) {
    this.$$set({ rtl: e }), G();
  }
  get text_align() {
    return this.$$.ctx[22];
  }
  set text_align(e) {
    this.$$set({ text_align: e }), G();
  }
  get autofocus() {
    return this.$$.ctx[23];
  }
  set autofocus(e) {
    this.$$set({ autofocus: e }), G();
  }
  get autoscroll() {
    return this.$$.ctx[24];
  }
  set autoscroll(e) {
    this.$$set({ autoscroll: e }), G();
  }
  get interactive() {
    return this.$$.ctx[25];
  }
  set interactive(e) {
    this.$$set({ interactive: e }), G();
  }
  get root() {
    return this.$$.ctx[26];
  }
  set root(e) {
    this.$$set({ root: e }), G();
  }
  get file_count() {
    return this.$$.ctx[27];
  }
  set file_count(e) {
    this.$$set({ file_count: e }), G();
  }
  get audio_btn() {
    return this.$$.ctx[28];
  }
  set audio_btn(e) {
    this.$$set({ audio_btn: e }), G();
  }
  get stop_audio_btn() {
    return this.$$.ctx[29];
  }
  set stop_audio_btn(e) {
    this.$$set({ stop_audio_btn: e }), G();
  }
  get rtc_configuration() {
    return this.$$.ctx[30];
  }
  set rtc_configuration(e) {
    this.$$set({ rtc_configuration: e }), G();
  }
  get time_limit() {
    return this.$$.ctx[31];
  }
  set time_limit(e) {
    this.$$set({ time_limit: e }), G();
  }
  get modality() {
    return this.$$.ctx[32];
  }
  set modality(e) {
    this.$$set({ modality: e }), G();
  }
  get mode() {
    return this.$$.ctx[33];
  }
  set mode(e) {
    this.$$set({ mode: e }), G();
  }
  get rtp_params() {
    return this.$$.ctx[34];
  }
  set rtp_params(e) {
    this.$$set({ rtp_params: e }), G();
  }
  get track_constraints() {
    return this.$$.ctx[35];
  }
  set track_constraints(e) {
    this.$$set({ track_constraints: e }), G();
  }
  get server() {
    return this.$$.ctx[36];
  }
  set server(e) {
    this.$$set({ server: e }), G();
  }
}
export {
  Gf as default
};
