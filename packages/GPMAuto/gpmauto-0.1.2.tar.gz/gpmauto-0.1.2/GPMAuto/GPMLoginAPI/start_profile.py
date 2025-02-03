from .GPMLoginAPI import GPMLoginAPI


# from GPMLoginAPI.GPMLoginAPI import GPMLoginAPI


class Profile(GPMLoginAPI):
    def __init__(self, profileId, apiUrl='http://127.0.0.1:19995') -> None:
        super().__init__(apiUrl)
        self.profileId = profileId
    def stop(self):
        return super().stop(self.profileId)
    def start(self, **kwargs):
        # print(kwargs)
        width = kwargs.setdefault("width", 500)
        height = kwargs.setdefault("height", 700)
        x = kwargs.setdefault("x", 0)
        y = kwargs.setdefault("y", 0)
        scale = kwargs.setdefault("scale", 1)
        proxy = kwargs.setdefault("proxy", None)
        extensions = kwargs.setdefault("extensions", None)
        addination_args = kwargs.setdefault("addination_args", [])
        if proxy: self.update(self.profileId, raw_proxy=proxy)
        try:
            args = ["--disable-popup-blocking", '--lang=en-us', "--disable-blink-features-AutomationControlled", "--disable-dev-shm-usage", '--no-first-run', '--no-service-autorun', '--password-store-basic']
            args.extend(addination_args)
            if extensions: args.append('--load-extension=%s'%extensions)
            startedResult = super().start(self.profileId, 
                                           addination_args=" ".join(args), 
                                           win_scale=scale, 
                                           win_pos="%s,%s"%(x, y), 
                                           win_size="%s,%s"%(width, height)
                                        )
            # print(startedResult)
            if not startedResult["success"]:
                return self.start(**kwargs)
            remote_debugging_address = str(startedResult["data"]["remote_debugging_address"])
            driver_path = str(startedResult["data"]["driver_path"])
            process_id = str(startedResult["data"]["process_id"])
            return {"remote_debugging_address": remote_debugging_address, "driver_path": driver_path, "process_id": process_id, "profile": self.get_profile(self.profileId)["data"]}
        except: 
            self.stop()
            return self.start(**kwargs)
# print(Profile("ddc899c8-e7b7-44c3-81f4-51a75133a761").start())